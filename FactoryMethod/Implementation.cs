namespace FactoryMethod
{
    // the interface of the product creation
    public abstract class DiscountService
    {
        public abstract int DiscountPercentage { get ; }

    }

    // the implements of the specific services
    public class CountryDiscountService : DiscountService
    {
        // we override the DiscountPercentage because it is uniqe to this class
        // here we need to implement our logic to calculate discount percent
        public override int DiscountPercentage { get => 25; }
    }

    public class CodeDiscountService : DiscountService
    {
        // we override the DiscountPercentage because it is uniqe to this class
        // here we need to implement our logic to calculate discount percent
        public override int DiscountPercentage { get => 50; }
    }

    // abstract factory
    public abstract class DiscountFactory
    {
        public abstract DiscountService CreateDiscountService();
    }

    // the implements of the specific factories
    public class CountryDiscountFactory : DiscountFactory
    {
        public override DiscountService CreateDiscountService()
        {
            return new CountryDiscountService();
        }
    }

    public class CodeDiscountFactory : DiscountFactory
    {
        public override DiscountService CreateDiscountService()
        {
            return new CodeDiscountService();
        }
    }
}
