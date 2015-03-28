const AUTHORIZATION_KEY = "3ul4VME1iusE8f5t4C3Fx7m39xOmJ49q";
const TEXT_URL = "http://127.0.0.1:5000/api/text/default";

(function() {
    
    var app = angular.module('quietEditor', [ ] );

    app.controller('editorController', ['$scope', '$sce', '$http', function($scope, $sce, $http) {

        // Call the API and handle the output.
        this.callBackend = function ( text ) {

            request = { auth : AUTHORIZATION_KEY };

            if ( text ) {
                request["text"] = text;
            }

            $http.post( TEXT_URL, request ).
                success(function(data, status, headers, config) {

                    // Populate the text area.
                    if ( data.text ) {
                        $scope.editor.textInput = data.text;
                    }

                    // Populate the preview.
                    if ( data.html ) {
                        $scope.renderedText = $sce.trustAsHtml(data.html);
                    }



                }).error(function(data, status, headers, config) {
                    alert("Could not reach server.");
            });

        }

        // Initialize by querying the server for what we have.
        this.callBackend();

        // Whenever there's new text, update the server.
        this.updateText = function( text ) {
            this.callBackend(text);
        }

    }]);


})();
