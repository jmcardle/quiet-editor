const AUTHORIZATION_KEY = "3ul4VME1iusE8f5t4C3Fx7m39xOmJ49q";
const TEXT_URL = "http://127.0.0.1:5000/api/text/";
const GET_TEXT = "get";
const SET_TEXT = "set";
const LIST_FILES = "list"
const LOAD_FILE = "load"
var current_file = "default"

$(function() {

    $('#input-text').scroll( function() {

        // Get the elements.
        var inputTextDiv = $('#input-text')[0];
        var renderedTextDiv = $('#rendered-text')[0];

        // Calculate where to scroll the rendered text to match where the input text is scrolled at.
        var percentScroll = ( inputTextDiv.scrollTop + inputTextDiv.offsetHeight ) / inputTextDiv.scrollHeight;
        var topPosition = renderedTextDiv.scrollHeight * percentScroll - renderedTextDiv.offsetHeight;
        topPosition = (topPosition < 0) ? 0 : topPosition;

        // Apply the scroll.
        renderedTextDiv.scrollTop = topPosition;
    });

});

(function() {

    var app = angular.module('quietEditor', [ 'toaster' ] );

    app.controller('editorController', ['$scope', '$sce', '$http', 'toaster', function($scope, $sce, $http, toaster) {

        // Call the API and handle the output.
        this.callBackend = function ( action, text ) {

            request = { auth : AUTHORIZATION_KEY, action : action };

            if ( text ) {
                request["text"] = text;
            }

            $http.post( TEXT_URL + current_file, request ).
                success(function(data, status, headers, config) {

                    // Populate the text area.
                    if ( action == GET_TEXT ) {
                        $scope.editor.inputText = data.text;
                    }

                    // Populate the preview.
                    $scope.renderedText = $sce.trustAsHtml(data.html);

                }).error(function(data, status, headers, config) {
                    toaster.pop('warning', "", "Could not reach server.");
            });

        }

        // Initialize by querying the server for what we have.
        this.callBackend(GET_TEXT);

        // Whenever there's new text, update the server.
        this.updateText = function( text ) {
            this.callBackend(SET_TEXT, text);
        }

        // When a command comes in, process it.
        this.runCommand = function( command ) {

            if ( command == LIST_FILES ) {
                this.callBackend(LIST_FILES);
                this.command = null;
            } else {
                toaster.pop('error', '', "Unrecognized command.");
            }

        }

    }]);

})();
