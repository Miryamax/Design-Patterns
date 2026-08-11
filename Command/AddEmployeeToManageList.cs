using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Command.Interfaces;

namespace Command
{
    public class AddEmployeeToManageList : ICommand
    {
        private readonly int managerId;
        private readonly Employee employee;
        private readonly IEmployeeManagerRepository employeeManagerRepository;

        public AddEmployeeToManageList(int managerId, Employee employee, IEmployeeManagerRepository employeeManagerRepository)
        {
            this.managerId = managerId;
            this.employee = employee;
            this.employeeManagerRepository = employeeManagerRepository;
        }

        public void Execute()
        {
           employeeManagerRepository.AddEmployeeToManagerList(managerId, employee);
        }
    }
}
