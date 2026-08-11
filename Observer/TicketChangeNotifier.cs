using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Observer.Interfaces;

namespace Observer
{
    public abstract class TicketChangeNotifier
    {
        private readonly List<ITicketChangeListener> observers = new List<ITicketChangeListener>();

        public void AddObserver(ITicketChangeListener observer)
        {
            observers.Add(observer);
        }

        public void RemoveObserver(ITicketChangeListener observer)
        {
            observers.Remove(observer);
        }

        public void Notify(TicketChange ticketChange)
        {
            foreach (var observer in observers)
            {
                observer.ReceiveTicketChangeNotification(ticketChange);
            }
        }
    }
}
