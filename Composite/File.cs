using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Composite
{
    // leaf
    public class File : FileSystemItem
    {
        public long Size { get; set; }

        public File(long size)
            { this.Size = size; }


        public override long GetSize()
        {
            return Size;
        }
    }
}
