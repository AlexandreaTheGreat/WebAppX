new Vue({
    el: '#app',
    data: {
      showEditModal: false,
      selectedDate: null,
      newTransaction: {
        Date: '',
        Name: '',
        Amount: '',
        Price: '',
        Type: null
      },
      transactions: [],
      showModal: false,
      editingTransaction: null,
      filterType: '',
      calendar: null,
    },
    mounted() {
      this.initializeCalendar();
      this.fetchScheduledTransactions();
    },

    methods: {
      fetchScheduledTransactions() {
        axios.get('http://127.0.0.1:5000/api/Scheduled')
          .then(response => {
            this.transactions = response.data.transactions;
            console.log(response.data.transactions);
            this.updateCalendarEvents();
          })
          .catch(error => {
            console.error('Error retrieving transactions:', error);
          });
      },
      initializeCalendar() {
        var calendarEl = document.getElementById('calendar');
        var vm = this; // Store the Vue instance reference
        this.calendar = new FullCalendar.Calendar(calendarEl, {
          dayCellContent: function (info) {
            var now = new Date();
            var currentMonth = now.getMonth();
            var cellMonth = info.date.getMonth();

            // Check if the cell's month is different from the current month
            if (cellMonth !== currentMonth) {
              // Add a custom CSS class to the cells that are not in the current month
              return { html: '<div class="grayed-out-day">' + info.dayNumberText + '</div>' };
            }

            return info.dayNumberText;
          },
          events: [],
          buttonText: {
            today: 'Today', // Text for the "today" button
            prev: 'Prev',
            next: 'Next'
          },
          dateClick: function (info) {
            // Call the openModal method to open the modal when a day is clicked
            vm.openModal(info.date);
          },
          eventClick: function (info) {
            console.log(info);
            vm.handleEventClick(info);
          }
          
        });
        this.calendar.render();
      },
      updateCalendarEvents() {
        // Create an array of FullCalendar events from your transactions data
        const events = this.transactions.map(transaction => ({
          id: transaction.id,
          title: transaction.Name,
          start: moment(transaction.Date).format('YYYY-MM-DD'), // Make sure this is in the correct format (e.g., '2023-10-31T10:00:00')
          // Add other event properties if necessary
        }));
        this.calendar.setOption('events', events);
      },
      updateEvent() {
        // Clone the editingTransaction to avoid modifying the original
        const updatedTransaction = { ...this.editingTransaction };
      
        // Update the transaction on the frontend
        const index = this.transactions.findIndex(transaction => transaction.id === this.editingTransaction.id);
        if (index !== -1) {
          this.transactions.splice(index, 1, updatedTransaction);
        }
      
        // Send a request to update the transaction on the backend
        axios.put(`http://127.0.0.1:5000/api/Scheduled/${this.editingTransaction.id}`, updatedTransaction)
          .then(response => {
            console.log(response.data.message);
          })
          .catch(error => {
            console.error('Error updating transaction:', error);
          });
      
        // Close the edit modal
        this.showEditModal = false;
        this.editingTransaction = null;
      },
      openModal(date) {
        this.selectedDate = date; // Store the selected date
        this.showModal = true; // Open the modal
      },
      addEvent() {
        // Create an event object with the form data
        const event = {
          title: this.newTransaction.Name,
          start: this.selectedDate,
          end: this.selectedDate, // Assuming the event is on the same day
          className: 'custom-event'
        };
        // Add the event to the calendar
        this.calendar.addEvent(event);
        this.newTransaction.Date = moment(this.selectedDate).format('YYYY-MM-DD');
        axios.post('http://127.0.0.1:5000/api/Scheduled', this.newTransaction)
        .then(response => {
          this.newTransaction = {
            Date: this.newTransaction.Date,
            Name: this.newTransaction.Name,
            Amount: this.newTransaction.Amount,
            Price: this.newTransaction.Price,
            Type: this.newTransaction.Type,
          };
        })
        .catch(error => {
          console.error('Error adding transaction:', error);
        });
        // Close the modal and reset the form
        this.showModal = false;
        this.newTransaction = {
          Name: '',
          Amount: '',
          Price: '',
          Type: ''
        };
      },

      handleEventClick(info) {
        // Find the event in the FullCalendar events array by eventId
        const event = this.transactions.find(transaction => transaction.id === info.event.id);
  
        if (event) {
          // Open the modal for editing
          this.showEditModal = true;
          this.editingTransaction = { ...event }; // Clone the event to avoid modifying the original
        }
      },
  
      // Add a new method to handle event deletion
      handleEventDelete() {
        // Find the index of the event in the FullCalendar events array by eventId
        const eventIndex = this.transactions.findIndex(transaction => transaction.id === this.editingTransaction.id);
  
        if (eventIndex !== -1) {
          // Remove the event from the FullCalendar events array
          this.transactions.splice(eventIndex, 1);
  
          // Remove the event from the calendar
          this.calendar.getEventById(this.editingTransaction.id).remove();
  
          // Send a request to delete the scheduled transaction from the backend
          axios.delete(`http://127.0.0.1:5000/api/Scheduled/${this.editingTransaction.id}`)
            .then(response => {
              console.log(response.data.message);
            })
            .catch(error => {
              console.error('Error deleting transaction:', error);
            });
  
          // Close the edit modal
          this.showEditModal = false;
          this.editingTransaction = null;
        }
      },
      
    },
  });
  