# WebAppX

<h1>Backend Code Overview</h1><br>
The backend code is written in Python using Flask, and it interacts with Firestore, a NoSQL database service provided by Google Cloud.
<h2>Fetching Transactions:</h2><br>
The /api/Transactions endpoint handles GET requests to retrieve transactions from the Firestore database.
The fetchTransactions() function retrieves transactions from Firestore and sends them as a JSON response. Transactions are categorized as either expenses or sales based on the Type field.

<br><h2>Adding Transactions:</h2><br>
The /api/Transactions endpoint handles POST requests to add new transactions.
The addTransaction() function validates the input data and adds the transaction to the Firestore database. The transaction is stored in both the general Transactions collection and either the Expenses or Sales collection based on the Type field.

<br><h2>Updating Transactions:</h2><br>
The /api/Transactions/<transaction_id> endpoint handles PUT requests to update existing transactions.
The updateTransaction(transaction_id) function updates the transaction in the Transactions collection. If the transaction type is changed, it is deleted from the current collection (either Expenses or Sales) and added to the appropriate collection based on the updated Type field.

<br><h2>Deleting Transactions:</h2><br>
The /api/Transactions/<transaction_id> endpoint handles DELETE requests to delete transactions.
The deleteTransaction(transaction_id) function deletes the transaction with the specified transaction_id from the Transactions collection.

<br><h2>Fetching Scheduled Transactions:</h2><br>
The /api/Scheduled endpoint handles GET requests to retrieve scheduled transactions from the Firestore database.
The get_sched_transactions() function retrieves scheduled transactions from the Scheduled collection in Firestore and sends them as a JSON response.

<br><h2>Scheduling Transactions:</h2><br>
The /api/Scheduled endpoint handles POST requests to schedule new transactions.
The schedule_transaction() function validates the input data and schedules the transaction in the Scheduled collection in Firestore.

<br><h1>Frontend Code Overview (Transaction Page)</h1><br>
The frontend code is implemented using Vue.js and interacts with the backend API to perform CRUD operations on transactions.

<br><h2>Displaying Transactions:</h2><br>
Transactions fetched from the backend are displayed in a table.
Transactions can be filtered based on search text and transaction type.

<br><h2>Adding Transactions:</h2><br>
Clicking the "Add Transaction" button opens a modal allowing users to input new transaction details.
The addTransaction() function sends a POST request to the backend to add the new transaction.

<br><h2>Editing Transactions:</h2><br>
Clicking the "Edit" button for a transaction opens a modal allowing users to edit transaction details.
The editTransaction(transaction) function populates the modal with the selected transaction's data.
The updateTransaction() function sends a PUT request to the backend to update the edited transaction.

<br><h2>Deleting Transactions:</h2><br>
Clicking the "Delete" button for a transaction sends a DELETE request to the backend to delete the transaction.

<br><h1>Frontend Code Overview (Calendar Page):</h1><br>

<h2>Displaying Scheduled Transactions on Calendar:</h2><br>
Scheduled transactions fetched from the backend are displayed as events on a calendar.
The initializeCalendar() function sets up the FullCalendar plugin to render the calendar.
The updateCalendarEvents() function formats the scheduled transactions as FullCalendar events and updates the calendar display.

<br><h2>Adding Scheduled Transactions:</h2><br>
Clicking a date on the calendar opens a modal allowing users to input new scheduled transaction details.
The addEvent() function creates a new event on the calendar and sends a POST request to the backend to schedule the transaction.
