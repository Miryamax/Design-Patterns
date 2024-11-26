using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace State
{
    public class RegularState : BankAccountState
    {
        public RegularState(BankAccount bankAccount)
        {
            State = bankAccount;
        }
        public override void Deposit(decimal amount)
        {
            Console.WriteLine($"deposit : {amount}\n from RegularState");
            //change state....
        }

        public override void WithDraw(decimal amount)
        {
            Console.WriteLine($"with draw : {amount}\n from RegularState");
            //change state....
        }
    }
}
