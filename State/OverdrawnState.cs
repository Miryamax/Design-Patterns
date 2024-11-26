using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace State
{
    public class OverdrawnState : BankAccountState
    {
        public OverdrawnState(BankAccount bankAccount)
        {
            State = bankAccount;
        }
        public override void Deposit(decimal amount)
        {
            Console.WriteLine($"deposit : {amount}\n from OverdrawnState");
            //change state....
        }

        public override void WithDraw(decimal amount)
        {
            Console.WriteLine($"with draw : {amount}\n from OverdrawnState");
            //change state....
        }
    }
}
