using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Observer
{
    public class OrderService : TicketChangeNotifier
    {
       
        public void CompleteTicketSale(int amount, int artistId)
        {
            // some logic
            Notify(new TicketChange(amount, artistId));
        }

        
    }
}
