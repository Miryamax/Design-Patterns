using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Command;

namespace Memento
{
    public class AddEmployeeToManagerListMemento
    {
        public int managerId { get; private set; }
        public Employee employee { get; private set; }

        public AddEmployeeToManagerListMemento(int _managerId, Employee _employee)
        {
            managerId = managerId;
            employee = _employee;
        }
    }
}
