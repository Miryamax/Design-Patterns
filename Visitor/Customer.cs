using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Visitor.Interfaces;

namespace Visitor
{
    public class Customer : IElement
    {
        public decimal Discount { get; set; }
        public void Accept(IVisitor visitor)
        {
            visitor.VisitCustomer(this);
        }
    }
}
