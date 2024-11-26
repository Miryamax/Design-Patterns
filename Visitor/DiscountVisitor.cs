using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Visitor.Interfaces;

namespace Visitor
{
    public class DiscountVisitor : IVisitor
    {
        public void VisitCustomer(Customer customer)
        {
            // here some specific logic to calculate the discount for the customer
            customer.Discount += 20;
        }

        public void VisitEmployee(Employee employee)
        {
            // here some specific logic to calculate the discount for the employee
            employee.Discount += 10;
        }
    }
}
