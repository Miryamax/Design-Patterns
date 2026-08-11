using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Composite
{
    // component
    public abstract class FileSystemItem
    {
        public abstract long GetSize();
    }
}
