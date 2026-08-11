using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ChainOfResponsibility.Interfaces;

namespace ChainOfResponsibility.classes
{
    public class DocumentApprovedByLigationHandler : IHandler<Document>
    {
        private IHandler<Document>? _successor;
        public void Handle(Document request)
        {
            // here some logic - validations
            // and go to the next handle
            _successor?.Handle(request);
        }

        public IHandler<Document> SetSuccessor(IHandler<Document> successor)
        {
            _successor = successor;
            return _successor;
        }
    }
}
