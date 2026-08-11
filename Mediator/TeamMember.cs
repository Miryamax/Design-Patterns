using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Mediator.Interfaces;

namespace Mediator
{
    public abstract class TeamMember
    {
        private IChatRoom? _room;
        public string Name { get; set; }

        protected TeamMember(string name)
        {
            Name = name;
        }

        public void SetChatRoom(IChatRoom chatRoom)
        {
            _room = chatRoom;
        }

        public void SendMessage(string message)
        {
            _room.SendMessage(message);
        }

        public void RecieveMessage(string message)
        {
            Console.WriteLine($"message {message}");
        }
    }
}
