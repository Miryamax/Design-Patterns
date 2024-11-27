using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Composite
{
    // composite
    public class Directory : FileSystemItem
    {
        public List<FileSystemItem> _items { get; set; }

        public Directory()
        {
            _items = new List<FileSystemItem>();
        }

        

        public override long GetSize()
        {
            long size = 0;
            foreach (var item in _items)
            {
                size += item.GetSize();
            }
            return size;
        }
    }
}
