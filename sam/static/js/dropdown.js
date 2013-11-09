$(document).ready(function() {

    /* home tabs */
    $('#subnav a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        $($(this).attr('href')).children().trigger('exposed', ['Custom', 'Event']);
    });
    

    /* deal with tab exposure */
    $('#published').on('exposed', function (event) {
        loadPublishedSpaces();
    });

    $('#unpublished').on('exposed', function (event) {
        loadUnpublishedSpaces();
    });

    $('#incomplete').on('exposed', function (event) {
        loadIncompleteSpaces();
    });

    var spacesLoadingCue = function (selector) {
        var tpl_src = $('#list-item-loading').html();

        window.location.hash = selector.substr(1) + '-spaces';
        $(selector).html(Handlebars.compile(tpl_src)());
    };

    var loadPublishedSpaces = function () {
        var selector = '#published';

        spacesLoadingCue(selector);

        $.ajax({
            url: window.spacescout_admin.app_url_root + 'api/v1/space/?published=1',
            dataType: 'json',
            error: ajaxSpaceError,
            success: function (data) {
                paintGroupings(selector, data);
            }
        });
    };

    var loadUnpublishedSpaces = function () {
        var selector = '#unpublished';

        spacesLoadingCue(selector);

        $.ajax({
            url: window.spacescout_admin.app_url_root + 'api/v1/space/?complete=1&published=0',
            dataType: 'json',
            error: ajaxSpaceError,
            success: function (data) {
                paintGroupings(selector, data);
            }
        });
    };
