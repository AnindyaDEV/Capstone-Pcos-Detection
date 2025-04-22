document.addEventListener('DOMContentLoaded', function () {
    // Initialize calendar if events exist
    const calendarEl = document.getElementById('calendar');
    if (calendarEl) {
      // Get events data from the hidden element
      const eventsData = JSON.parse(document.getElementById('events-data').textContent);
      
      const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: eventsData,
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,dayGridWeek'
        },
        dayCellDidMount: function (info) {
          const period = info.el.getAttribute('data-period');
          if (period) {
            info.el.setAttribute('data-period', period);
          }
        }
      });
      
      calendar.render();
      
      // Set initial date to last period date if available
      const lastPeriod = document.getElementById('last-period-value').textContent;
      if (lastPeriod) {
        calendar.gotoDate(lastPeriod);
      }
    }
  
    // Export functionality
    document.getElementById('downloadIcal')?.addEventListener('click', function() {
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = '/download_ical';
      
      const addInput = (name, value) => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = value;
        form.appendChild(input);
      };
      
      addInput('last_period', document.getElementById('last_period').value);
      addInput('period_length', document.getElementById('period_length').value);
      addInput('cycle_length', document.getElementById('cycle_length').value);
      
      document.body.appendChild(form);
      form.submit();
    });
    
    // Calendar integration
    document.getElementById('addToCalendar')?.addEventListener('click', function() {
      const modal = new bootstrap.Modal(document.getElementById('calendarModal'));
      modal.show();
      
      const lastPeriod = document.getElementById('last_period').value;
      const periodLength = parseInt(document.getElementById('period_length').value);
      const cycleLength = parseInt(document.getElementById('cycle_length').value);
      
      const startDate = new Date(lastPeriod);
      const endDate = new Date(startDate);
      endDate.setDate(endDate.getDate() + periodLength);
      
      const ovulationDate = new Date(startDate);
      ovulationDate.setDate(ovulationDate.getDate() + cycleLength - 16);
      
      const formatDate = (date) => date.toISOString().replace(/-|:|\.\d+/g, '');
      
      document.getElementById('googleCalendar').href = 
        `https://www.google.com/calendar/render?action=TEMPLATE` +
        `&text=Period` +
        `&dates=${formatDate(startDate)}/${formatDate(endDate)}` +
        `&details=Menstrual+period` +
        `&location=&sprop=&sprop=name:`;
      
      document.getElementById('outlookCalendar').href = 
        `https://outlook.live.com/calendar/0/deeplink/compose` +
        `?startdt=${startDate.toISOString()}` +
        `&enddt=${endDate.toISOString()}` +
        `&subject=Period` +
        `&body=Menstrual+period`;
      
      document.getElementById('appleCalendar').href = 
        `webcal://harmony-tracker.com/calendar.ics`;
    });
  });