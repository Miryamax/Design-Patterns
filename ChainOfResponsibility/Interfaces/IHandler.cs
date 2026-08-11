using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChainOfResponsibility.Interfaces
{
    public interface IHandler<T>
    {
        void Handle(T request);

        IHandler<T> SetSuccessor(IHandler<T> successor);
    }
}
