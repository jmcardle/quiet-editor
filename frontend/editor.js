const AUTHORIZATION_KEY = "3ul4VME1iusE8f5t4C3Fx7m39xOmJ49q";
const TEXT_URL = "http://127.0.0.1:5000/api/text/default";
const GET_TEXT = "get";
const SET_TEXT = "set";

document.addEventListener('DOMContentLoaded', documentReady, false);

function documentReady(){
    document.getElementById("input-text").addEventListener("scroll", syncRenderedTextScrollBarToInputText);
}

function syncRenderedTextScrollBarToInputText() {
    var inputTextDiv = document.getElementById("input-text");
    var renderedTextDiv = document.getElementById("rendered-text");
    var percentScroll = ( inputTextDiv.scrollTop + inputTextDiv.offsetHeight ) / inputTextDiv.scrollHeight;
    var topPosition = renderedTextDiv.scrollHeight * percentScroll - renderedTextDiv.offsetHeight;
    topPosition = (topPosition < 0) ? 0 : topPosition;
    renderedTextDiv.scrollTop = topPosition;
}

(function() {
    
    var app = angular.module('quietEditor', [ 'toaster' ] );

    app.controller('editorController', ['$scope', '$sce', '$http', 'toaster', function($scope, $sce, $http, toaster) {

        // Call the API and handle the output.
        this.callBackend = function ( action, text ) {

            request = { auth : AUTHORIZATION_KEY, action : action };

            if ( text ) {
                request["text"] = text;
            }

            $http.post( TEXT_URL, request ).
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

    }]);


})();
