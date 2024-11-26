using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace State
{
    public abstract class BankAccountState
    {
        public BankAccount State { get; set; }

        public abstract void Deposit(decimal amount);

        public abstract void WithDraw(decimal amount);
    }
}
