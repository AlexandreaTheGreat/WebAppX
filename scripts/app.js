var app = angular.module('myApp', []);
const url = 'http://127.0.0.1:5000/api/Transactions';


app.controller('TransactionController', function($scope, $http) {
    $scope.newTransaction = {
        Date: '',
        Name: '',
        Amount: '',
        Price: '',
        Type: ''
    };
    $scope.showModal = false;

    // Fetch transactions
    $scope.fetchTransactions = function() {
        $http.get(url)
            .then(function(response) {
                $scope.transactions = response.data.transactions;
            })
            .catch(function(error) {
                console.error('Error retrieving transactions:', error);
            });
    };

    // Initial fetch
    $scope.fetchTransactions();

    // Function to add a new transaction
    $scope.addTransaction = function(newTransaction) {
        $http.post(url, newTransaction)
            .then(function(response) {
                // Clear form fields after adding a transaction
                $scope.newTransaction = {
                    Date: '',
                    Name: '',
                    Amount: '',
                    Price: '',
                    Type: ''
                };
                $scope.fetchTransactions();
                // Close the modal after adding the transaction
                $scope.showModal = false;
                $scope.$apply();
            })
            .catch(function(error) {
                console.error('Error adding transaction:', error);
            });
    };

    // Function to delete a transaction
    $scope.deleteTransaction = function(transactionId) {
        $http.delete(url + '/' + transactionId)
            .then(function(response) {
                $scope.fetchTransactions();
                $scope.$apply();
            })
            .catch(function(error) {
                console.error('Error deleting transaction:', error);
            });
    };

    // Function to edit a transaction
    $scope.editingTransaction = null;

    // Function to set data for editing
    $scope.editTransaction = function(transaction) {
        // Set the editingTransaction object to the selected transaction's data
        $scope.editingTransaction = angular.copy(transaction);
        $scope.editingTransaction.Date = new Date(transaction.Date);
        $scope.showEditModal = true;
    };

    // Function to update a transaction
    $scope.updateTransaction = function() {
        // Make a PUT request to update the transaction
        $http.put(url + '/' + $scope.editingTransaction.id, $scope.editingTransaction)
            .then(function(response) {
                // Handle success, maybe refresh the transaction list
                console.log('Transaction updated successfully');
                
                // Close the modal after updating the transaction
                $scope.showEditModal = false;

                // Reset the editingTransaction object
                $scope.editingTransaction = null;
                $scope.fetchTransactions();
                $scope.$apply();
            })
            .catch(function(error) {
                console.error('Error updating transaction:', error);
            });
    };


    $scope.filterType = '';
    $scope.filterTransactions = function(transaction) {
        if (!$scope.filterType) {
            // If filterType is not selected, show all transactions
            return true;
        } else {
            // Show transactions based on selected filterType
            return transaction.Type == $scope.filterType;
        }
    };
});
