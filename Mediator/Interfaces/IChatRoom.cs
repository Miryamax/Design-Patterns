using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Mediator.Interfaces
{
    public interface IChatRoom
    {
        void AddMember(TeamMember member);
        void SendMessage(string message);
    }
}
