new Vue({
    el: '#app',
    data: {
      searchText: '',
      showEditModal: false,
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
    },
    mounted() {
      this.fetchTransactions();
    },
    computed: {
      filteredTransactions() {
        return this.transactions.filter(transaction => this.filterTransactions(transaction));
      }
    },
    methods: {
      fetchTransactions() {
        axios.get('http://127.0.0.1:5000/api/Transactions')
          .then(response => {
            this.transactions = response.data.transactions;
            console.log(response.data.transactions);
          })
          .catch(error => {
            console.error('Error retrieving transactions:', error);
          });
      },
      addTransaction() {
        axios.post('http://127.0.0.1:5000/api/Transactions', this.newTransaction)
          .then(response => {
            this.newTransaction = {
              Date: '',
              Name: '',
              Amount: '',
              Price: '',
              Type: ''
            };
            this.fetchTransactions();
            this.showModal = false;
          })
          .catch(error => {
            console.error('Error adding transaction:', error);
          });
      },
      deleteTransaction(transactionId) {
        axios.delete(`http://127.0.0.1:5000/api/Transactions/${transactionId}`)
          .then(response => {
            this.fetchTransactions();
          })
          .catch(error => {
            console.error('Error deleting transaction:', error);
          });
      },
      editTransaction(transaction) {
        const formattedDate = new Date(transaction.Date).toISOString().slice(0, 10);
        console.log(this.editingTransaction);
        this.editingTransaction = {
          id: transaction.id,
          ID: transaction.ID,
          Date: formattedDate,
          Name: transaction.Name,
          Amount: transaction.Amount,
          Price: transaction.Price,
          Type: transaction.Type,
        };
        this.showEditModal = true;
      },
      updateTransaction() {
        console.log('Updating transaction:', this.editingTransaction);
        axios.put(`http://127.0.0.1:5000/api/Transactions/${this.editingTransaction.id}`, this.editingTransaction)
          .then(response => {
            console.log('Transaction updated successfully');
            this.showEditModal = false;
            this.editingTransaction = null;
            this.fetchTransactions();
          })
          .catch(error => {
            console.error('Error updating transaction:', error);
          });
      },
      filterTransactions(transaction) {
        const matchesType = !this.filterType || transaction.Type == this.filterType;
        const matchesSearch = !this.searchText || transaction.Name.toLowerCase().includes(this.searchText.toLowerCase());
        return matchesType && matchesSearch;
      }
    }
  });
  