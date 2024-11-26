using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace State
{
    public abstract class BankAccount
    {
        public BankAccountState BankAccountState { get; set;  }

        public BankAccount(BankAccountState bankAccountState)
        {
            BankAccountState = bankAccountState;
        }
        public void Deposit(decimal amount)
        {
            BankAccountState.Deposit(amount);
        }

        public void WithDraw(decimal amount)
        {
            BankAccountState.WithDraw(amount);
        }
    }
}
