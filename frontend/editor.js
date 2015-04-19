const AUTHORIZATION_KEY = "3ul4VME1iusE8f5t4C3Fx7m39xOmJ49q";
const TEXT_URL = "http://127.0.0.1:5000/api/text/";
const GET_TEXT = "get";
const SET_TEXT = "set";
const LIST_FILES = "list";
const LOAD_FILE = "load";
const TRASH_FILE = "trash";
const RESTORE_FILE = "restore";
const HELP = "help";
const STORAGE_ACTIVE_FILE = "active-file";
const DEFAULT_FILE = "default";

function setActiveFile( filename ) {

    localStorage.setItem( STORAGE_ACTIVE_FILE, filename );

}

function getActiveFile( filename ) {

    var activeFile = localStorage.getItem(STORAGE_ACTIVE_FILE);

    return activeFile ? activeFile : DEFAULT_FILE;

}

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
        this.callBackend = function ( action, file, arguments ) {

            request = { auth : AUTHORIZATION_KEY, action : action };

            // Send the arguments in the request.
            for (var key in arguments) {
                request[key] = arguments[key];
            }

            $http.post( TEXT_URL + file, request ).
                success(function(data, status, headers, config) {

                    // Populate the text area.
                    if ( action == GET_TEXT ) {
                        $scope.editor.inputText = data.text;
                    }

                    // Put up a message if one was received.
                    if ( data.info ) {
                        toaster.pop('info', "", data.info);
                    }

                    if ( data.error ) {
                        toaster.pop('warning', "", data.error);
                    }

                    // Populate the preview
                    if ( data.html || action == GET_TEXT || action == SET_TEXT ) {
                        $scope.renderedText = $sce.trustAsHtml(data.html);
                    }

                }).error(function(data, status, headers, config) {
                    toaster.pop('warning', "", "Could not reach server.");
            });

        }

        // Initialize by querying the server for what we have.
        this.callBackend( GET_TEXT, getActiveFile() );

        // Whenever there's new text, update the server.
        this.updateText = function( text ) {
            this.callBackend( SET_TEXT, getActiveFile(), { text : text });
        }

        // When a command comes in, process it.
        this.runCommand = function( userInput ) {

            var firstSpace = userInput.indexOf(" ");
            var command = (firstSpace >= 0) ? userInput.substring(0, firstSpace) : userInput;
            var arguments = (firstSpace >= 0) ? userInput.substring(firstSpace + 1).trim() : "";


            if ( command == HELP ) {

                toaster.pop('info', 'Commands', "help, list, list trash, load, trash, restore");
                this.command = null;

            } else if ( command == LIST_FILES ) {

                var arguments = ( arguments == "trash" ) ? "trash" : "all";
                this.callBackend( LIST_FILES, arguments );
                this.command = null;

            } else if ( command == LOAD_FILE ) {

                setActiveFile( arguments )
                this.callBackend( GET_TEXT, getActiveFile() );
                this.command = null;

            } else if ( command == TRASH_FILE ) {

                this.callBackend( TRASH_FILE, arguments );
                this.command = null;

            } else if ( command == RESTORE_FILE ) {

                this.callBackend( RESTORE_FILE, arguments );
                this.command = null;

            } else {

                toaster.pop('error', '', "Unrecognized command.");

            }

        }

    }]);

})();
