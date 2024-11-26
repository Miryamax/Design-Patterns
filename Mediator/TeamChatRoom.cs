using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Mediator.Interfaces;

namespace Mediator
{
    public class TeamChatRoom : IChatRoom
    {
        private readonly List<TeamMember> members = new();

        public void AddMember(TeamMember member)
        {
            member.SetChatRoom(this);
            if (!members.Contains(member)) 
                members.Add(member);
        }

        public void SendMessage(string message)
        {
            foreach (var teamMember in members)
            {
                teamMember.RecieveMessage(message);
            }
        }

       
    }
}
