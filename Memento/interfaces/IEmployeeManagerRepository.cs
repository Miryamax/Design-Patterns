using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Command.Interfaces
{
    public interface IEmployeeManagerRepository
    {
        void AddEmployeeToManagerList(int managerId, Employee employee);


        // here more functions we will want to do on the manager list
    }
}
