using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Iterator.Interfaces
{
    public interface IPeopleIterator
    {
        Person First();
        Person Next();
        bool IsDone();
        Person CurrentItem { get; }
    }
}
