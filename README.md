# WebAppX

<h1>Backend Code Overview</h1><br>
The backend code is written in Python using Flask, and it interacts with Firestore, a NoSQL database service provided by Google Cloud.
<h2>Fetching Transactions:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/32b204ce-1002-4288-9e90-309ab8d4f289)
The /api/Transactions endpoint handles GET requests to retrieve transactions from the Firestore database.
The fetchTransactions() function retrieves transactions from Firestore and sends them as a JSON response. Transactions are categorized as either expenses or sales based on the Type field.

<br><h2>Adding Transactions:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/3281e3c7-08dd-43e4-86af-19d7a7dbdbc0)
The /api/Transactions endpoint handles POST requests to add new transactions.
The addTransaction() function validates the input data and adds the transaction to the Firestore database. The transaction is stored in both the general Transactions collection and either the Expenses or Sales collection based on the Type field.

<br><h2>Updating Transactions:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/107d542e-5237-44ff-8e07-7cd693c7d77d)
The /api/Transactions/<transaction_id> endpoint handles PUT requests to update existing transactions.
The updateTransaction(transaction_id) function updates the transaction in the Transactions collection. If the transaction type is changed, it is deleted from the current collection (either Expenses or Sales) and added to the appropriate collection based on the updated Type field.

<br><h2>Deleting Transactions:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/d1e3b618-e19e-4a4f-8cdf-1778191b7271)
The /api/Transactions/<transaction_id> endpoint handles DELETE requests to delete transactions.
The deleteTransaction(transaction_id) function deletes the transaction with the specified transaction_id from the Transactions collection.

<br><h2>Fetching Scheduled Transactions:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/6f7c328b-26df-43fb-90f3-d8ebddf303a2)
The /api/Scheduled endpoint handles GET requests to retrieve scheduled transactions from the Firestore database.
The get_sched_transactions() function retrieves scheduled transactions from the Scheduled collection in Firestore and sends them as a JSON response.

<br><h2>Scheduling Transactions:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/22a93846-cda3-4f03-b756-590c8041f408)
The /api/Scheduled endpoint handles POST requests to schedule new transactions.
The schedule_transaction() function validates the input data and schedules the transaction in the Scheduled collection in Firestore.

<br><h1>Frontend Code Overview (Transaction Page)</h1><br>
The frontend code is implemented using Vue.js and interacts with the backend API to perform CRUD operations on transactions.

<br><h2>Displaying Transactions:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/e7f78327-975b-405b-b7aa-f73e97ea61c5)
Transactions fetched from the backend are displayed in a table.
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/7f486c95-38ad-4a51-b7a1-839629b8ecfe)
Transactions can be filtered based on search text and transaction type.

<br><h2>Adding Transactions:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/68f50269-ca6e-41b1-99fa-93e6563b241a)
Clicking the "Add Transaction" button opens a modal allowing users to input new transaction details.
The addTransaction() function sends a POST request to the backend to add the new transaction.

<br><h2>Editing Transactions:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/562112a6-5315-4244-9be9-082e53cf2071)
Clicking the "Edit" button for a transaction opens a modal allowing users to edit transaction details.
The editTransaction(transaction) function populates the modal with the selected transaction's data.
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/ac39fa91-b7ee-4265-9f4f-592a537f97e1)
The updateTransaction() function sends a PUT request to the backend to update the edited transaction.

<br><h2>Deleting Transactions:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/11d47f33-fef6-4f53-8ee9-9e475ba76f5a)
Clicking the "Delete" button for a transaction sends a DELETE request to the backend to delete the transaction.

<br><h1>Frontend Code Overview (Calendar Page):</h1><br>

<h2>Displaying Scheduled Transactions on Calendar:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/91f53fc1-f439-4cc0-8ab9-de734f4a0c0b)
Scheduled transactions fetched from the backend are displayed as events on a calendar.
The initializeCalendar() function sets up the FullCalendar plugin to render the calendar.
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/8df7db45-ed3a-4588-a644-b5317a481ef5)
The updateCalendarEvents() function formats the scheduled transactions as FullCalendar events and updates the calendar display.

<br><h2>Adding Scheduled Transactions:</h2><br>
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/c5b50aff-29ef-478b-8fd4-b6a7d3cf13a5)
Clicking a date on the calendar opens a modal allowing users to input new scheduled transaction details.
![image](https://github.com/AlexandreaTheGreat/WebAppX/assets/134761954/07d9185e-3fae-4318-98ba-1b987ec02c9a)
The addEvent() function creates a new event on the calendar and sends a POST request to the backend to schedule the transaction.
