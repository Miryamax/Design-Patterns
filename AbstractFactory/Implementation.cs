namespace AbstractFactory
{
    // the interfaces of our products / services
    public interface IDiscountService
    {
        public int DiscountPercentage { get; }
    }

    public interface IShippingCostService
    {
        public  decimal ShippingCost { get;  }
    }

    // the specific classes of the services
    public class BelguimDiscountService : IDiscountService
    {
        // some logic...
        public int DiscountPercentage { get => 10; }

    }

    public class FrenchDiscountService : IDiscountService
    {
        // some logic...
        public int DiscountPercentage { get => 20; }

    }

    public class BelguimShippingCostService : IShippingCostService
    {
        // some logic...
        public decimal ShippingCost { get => 50; }
    }

    public class FrenchShippingCostService : IShippingCostService
    {
        // some logic...
        public decimal ShippingCost { get => 40; }
    }

    // the abstract factory - here all the family will be
    public interface IShoppingCartPurchaseFactory
    {
        public  IShippingCostService CreateShippingCostService();
        public  IDiscountService CreateDiscountService();

    }

    // the implement factory 
    public class BelguimShoppingCartPurchaseFactory : IShoppingCartPurchaseFactory
    {
        public IShippingCostService CreateShippingCostService()
        {
            return new BelguimShippingCostService();
        }

        public IDiscountService CreateDiscountService()
        {
            return new BelguimDiscountService();
        }
    }

    public class FrenchShoppingCartPurchaseFactory : IShoppingCartPurchaseFactory
    {
        public IShippingCostService CreateShippingCostService()
        {
            return new FrenchShippingCostService();
        }

        public IDiscountService CreateDiscountService()
        {
            return new FrenchDiscountService();
        }
    }

    // the client
    public class ShoppingCart
    {
        private readonly IShoppingCartPurchaseFactory _factory;
        public ShoppingCart(IShoppingCartPurchaseFactory factory)
        {
            this._factory = factory;
        }

        public void CalculateCosts()
        {
            Console.WriteLine("calculate.......");
        }
    }
}
