using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Command.Interfaces;

namespace Command
{
    public class EmployeeManagerRepository : IEmployeeManagerRepository
    {
        
        private List<Manager> _managers = new List<Manager>();

        public void AddEmployeeToManagerList(int managerId, Employee employee)
        {
            _managers.Find(k=> k.Id == managerId).employees.Add(employee);
        }

        // imagine that here more functions...

        
    }
}
