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
    $scope.editTransaction = function(transactionId) {
        // Implement edit transaction logic here using API PUT request
    };
});
