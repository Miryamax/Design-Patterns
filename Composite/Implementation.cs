namespace Composite
{
    // component
    public abstract class FileSystemItem
    {
        public abstract long GetSize();
    }

    // leaf
    public class File : FileSystemItem
    {
        public override long GetSize()
        {
            return 39;
        }
    }

    // composite
    public class Directory : FileSystemItem
    {
        private List<FileSystemItem> _items;

        public override long GetSize()
        {
            long size  = 0;
            foreach (var item in _items)
            {
                size += item.GetSize();
            }
            return size;
        }
    }
}
