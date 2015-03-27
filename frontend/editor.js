(function() {
    
    var app = angular.module('quietEditor', [ ] );

    app.controller('editorController', ['$scope', '$sce', function($scope, $sce) {

        this.renderText = function( text ) {
            
            $scope.renderedText = $sce.trustAsHtml(toMarkdown(text));
        }
    
    }]);
    

})();


function toMarkdown( text ) {
    
    // Sanitize HTML.
    var output = "<p>";
    for ( i=0; i < text.length; i++) {

        var lastCharIsNewline = false;
    
        switch ( text.charAt( i ) ) {
            case "<":
                output += "<h2>";
                break;
            case ">":
                output += "</h2>";
                break;
            case "[":
                output += "<blockquote><p>";
                break;
            case "]":
                output += "</p></blockquote>";
                break;
            case "{":
                output += "<em>";
                break;
            case "}":
                output += "</em>";
                break;
            case "\n":
                if (!lastCharIsNewline) {
                    output += "</p><p>";
                    lastCharIsNewline = true;
                }
                break;
            case "\r":
                break;
            default:
                output += text.charAt( i );
                lastCharIsNewline = false;
        } 
    }
    
    output += "</p>";
    
    return output;    
}