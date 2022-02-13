/*!
 * FullCalendar v3.1.0 Stylesheet
 * Docs & License: http://fullcalendar.io/
 * (c) 2016 Adam Shaw
 */

$(function () { 

    var calendar = $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month, agendaWeek,agendaDay,listMonth'
        },

        defaultTimedEventDuration: '00:30',
        navLinks: true, // can click day/week names to navigate views
        editable: true,
        eventLimit: true, // allow "more" link when too many events

        events: [ {
            title: 'All Day Event',
            start: '2021-11-01'
        },
        {
            title: 'Few day Event',
            start: '2021-11-07',
            end: '2021-11-10'
        },
        {
            id: 999,
            title: 'Repeating Event',
            start: '2021-11-09T16:00:00'
        },
        {
            id: 999,
            title: 'Repeating Event',
            start: '2021-11-16T16:00:00'
        },
        {
            title: 'Conference',
            start: '2021-11-11',
            end: '2021-11-13'
        },
        {
            title: 'Meeting',
            start: '2021-11-11T10:30:00',
            end: '2021-11-11T11:30:00'
        },
        {
            title: 'Lunch',
            start: '2021-11-11T11:00:00'
        },
        {
            title: 'Meeting',
            start: '2021-11-11T14:30:00'
        },
        {
            title: 'Happy Hour',
            start: '2021-11-11T17:30:00'
        },
        {
            title: 'Dinner',
            start: '2021-11-11T20:00:00'
        },
        {
            title: 'Birthday Party',
            start: '2021-11-13T07:00:00'
        },
        {
            title: 'Click for Google',
            url: 'https://google.com/',
            start: '2021-11-28'
        }],
        
        selectable: true,
        select: function (start, end) {
            var duration = (end - start) / 1000;
            if (duration == 1800) {
                // set default duration to 1 hr.
                end = start.add(30, 'mins');
                return calendar.fullCalendar('select', start, end);
            }
            var title = prompt('Event Title:');
            var eventData;
            if (title && title.trim()) {
                eventData = {
                    title: title,
                    start: start,
                    end: end
                };
                calendar.fullCalendar('renderEvent', eventData);
            }
            calendar.fullCalendar('unselect');
        },
        //  When hovering over an event, it will display how long ago the event either happened or how soon it will happen from current date.
        eventRender: function (event, element) {
            var start = moment(event.start).fromNow();
            element.attr('title', start);
        },
        loading: function () {

        }
    });

});