using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Visitor.Interfaces
{
    public interface IVisitor
    {
        // the visitor functions 
        void VisitCustomer(Customer customer);
        void VisitEmployee(Employee employee);
    }
}
