// Marketplace Product Data
const products = [
  // Electronics
  {
    item_id: "1001",
    item_name: "Wireless Bluetooth Headphones",
    category: "electronics",
    price: 79.99,
    brand: "SoundTech",
    description: "Premium wireless headphones with noise cancellation and 30-hour battery life. Perfect for music lovers and professionals.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Premium%20wireless%20bluetooth%20headphones%20with%20noise%20cancellation%20sleek%20modern%20design%20black%20and%20silver%20professional%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "1002",
    item_name: "4K Webcam Pro",
    category: "electronics",
    price: 129.99,
    brand: "VisionCam",
    description: "Crystal clear 4K webcam with auto-focus and built-in microphone. Ideal for video conferencing and streaming.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Professional%204K%20webcam%20sleek%20black%20design%20with%20auto-focus%20lens%20modern%20tech%20product%20photography%20clean%20background&image_size=square_hd"
  },
  {
    item_id: "1003",
    item_name: "Smartphone Stand",
    category: "electronics",
    price: 24.99,
    brand: "HoldIt",
    description: "Adjustable aluminum smartphone stand with 360-degree rotation. Perfect for desk or bedside table.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Adjustable%20aluminum%20smartphone%20stand%20modern%20minimalist%20design%20silver%20finish%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "1004",
    item_name: "Wireless Mouse",
    category: "electronics",
    price: 45.99,
    brand: "ClickPro",
    description: "Ergonomic wireless mouse with precision tracking and long battery life. Comfortable for extended use.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Ergonomic%20wireless%20mouse%20modern%20design%20black%20and%20gray%20precision%20tracking%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "1005",
    item_name: "USB-C Hub",
    category: "electronics",
    price: 59.99,
    brand: "ConnectAll",
    description: "7-in-1 USB-C hub with HDMI, USB 3.0, SD card reader, and PD charging. Essential for modern laptops.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=7-in-1%20USB-C%20hub%20modern%20sleek%20design%20multiple%20ports%20professional%20product%20photography&image_size=square_hd"
  },

  // Fashion
  {
    item_id: "2001",
    item_name: "Classic Cotton T-Shirt",
    category: "fashion",
    price: 29.99,
    brand: "ComfortWear",
    description: "100% organic cotton t-shirt with classic fit. Soft, breathable, and perfect for everyday wear.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Classic%20cotton%20t-shirt%20white%20color%20clean%20minimalist%20style%20fashion%20product%20photography%20professional%20lighting&image_size=square_hd"
  },
  {
    item_id: "2002",
    item_name: "Denim Jacket",
    category: "fashion",
    price: 89.99,
    brand: "DenimCo",
    description: "Timeless denim jacket with modern fit. Perfect layering piece for any season.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Classic%20denim%20jacket%20blue%20wash%20modern%20fit%20fashion%20product%20photography%20professional%20lighting&image_size=square_hd"
  },
  {
    item_id: "2003",
    item_name: "Running Shoes",
    category: "fashion",
    price: 119.99,
    brand: "RunFast",
    description: "Lightweight running shoes with advanced cushioning technology. Perfect for daily training or casual wear.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Modern%20running%20shoes%20white%20and%20blue%20design%20athletic%20style%20product%20photography%20clean%20background&image_size=square_hd"
  },
  {
    item_id: "2004",
    item_name: "Leather Belt",
    category: "fashion",
    price: 49.99,
    brand: "LeatherCraft",
    description: "Genuine leather belt with classic buckle. Timeless accessory that complements any outfit.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Genuine%20leather%20belt%20brown%20color%20classic%20buckle%20fashion%20accessory%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "2005",
    item_name: "Wool Scarf",
    category: "fashion",
    price: 34.99,
    brand: "WarmStyle",
    description: "Soft wool scarf with elegant pattern. Perfect for cold weather and adds sophisticated touch to any outfit.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Soft%20wool%20scarf%20gray%20and%20navy%20pattern%20elegant%20design%20fashion%20accessory%20product%20photography&image_size=square_hd"
  },

  // Books
  {
    item_id: "3001",
    item_name: "The Art of Programming",
    category: "books",
    price: 45.99,
    brand: "TechBooks",
    description: "Comprehensive guide to modern programming techniques. Essential for developers and computer science students.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Programming%20book%20cover%20modern%20design%20clean%20typography%20blue%20and%20white%20color%20scheme%20professional%20book%20cover&image_size=square_hd"
  },
  {
    item_id: "3002",
    item_name: "Mystery Novel Collection",
    category: "books",
    price: 24.99,
    brand: "StoryPress",
    description: "Collection of thrilling mystery stories. Perfect for readers who love suspense and unexpected plot twists.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Mystery%20novel%20book%20cover%20dark%20atmospheric%20design%20mysterious%20typography%20black%20and%20red%20color%20scheme&image_size=square_hd"
  },
  {
    item_id: "3003",
    item_name: "Cooking Masterclass",
    category: "books",
    price: 39.99,
    brand: "CulinaryArts",
    description: "Professional cooking techniques and recipes from world-renowned chefs. Transform your kitchen skills.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Cooking%20book%20cover%20vibrant%20food%20photography%20clean%20modern%20design%20warm%20colors%20professional%20cookbook%20cover&image_size=square_hd"
  },
  {
    item_id: "3004",
    item_name: "Business Strategy Guide",
    category: "books",
    price: 54.99,
    brand: "BusinessPro",
    description: "Essential strategies for business success. Learn from industry leaders and apply proven methodologies.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Business%20strategy%20book%20cover%20professional%20design%20corporate%20blue%20color%20scheme%20clean%20typography%20modern%20business%20book&image_size=square_hd"
  },
  {
    item_id: "3005",
    item_name: "Art History Illustrated",
    category: "books",
    price: 67.99,
    brand: "ArtPress",
    description: "Beautifully illustrated journey through art history. Perfect for art enthusiasts and students.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Art%20history%20book%20cover%20elegant%20design%20classic%20artwork%20sophisticated%20typography%20gold%20and%20navy%20color%20scheme&image_size=square_hd"
  },

  // Beauty
  {
    item_id: "4001",
    item_name: "Hydrating Face Cream",
    category: "beauty",
    price: 32.99,
    brand: "GlowSkin",
    description: "Rich moisturizing cream with hyaluronic acid and vitamins. Leaves skin soft, smooth, and radiant.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Luxury%20face%20cream%20jar%20elegant%20packaging%20white%20and%20gold%20design%20beauty%20product%20photography%20clean%20background&image_size=square_hd"
  },
  {
    item_id: "4002",
    item_name: "Vitamin C Serum",
    category: "beauty",
    price: 45.99,
    brand: "BrightGlow",
    description: "Powerful antioxidant serum with 20% vitamin C. Brightens skin and reduces signs of aging.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Vitamin%20C%20serum%20bottle%20amber%20glass%20with%20dropper%20clean%20beauty%20packaging%20professional%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "4003",
    item_name: "Natural Lip Balm Set",
    category: "beauty",
    price: 18.99,
    brand: "SoftLips",
    description: "Set of 3 organic lip balms with different flavors. Moisturizing formula with natural ingredients.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Natural%20lip%20balm%20set%20colorful%20tubes%20organic%20packaging%20pastel%20colors%20beauty%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "4004",
    item_name: "Mineral Foundation",
    category: "beauty",
    price: 38.99,
    brand: "PureMinerals",
    description: "Lightweight mineral foundation with natural coverage. Perfect for sensitive skin and everyday wear.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Mineral%20foundation%20powder%20compact%20elegant%20packaging%20neutral%20tones%20beauty%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "4005",
    item_name: "Rose Water Toner",
    category: "beauty",
    price: 22.99,
    brand: "RoseGarden",
    description: "Gentle rose water toner that refreshes and balances skin. Made with organic rose petals.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Rose%20water%20toner%20glass%20bottle%20with%20spray%20elegant%20packaging%20pink%20tones%20beauty%20product%20photography&image_size=square_hd"
  },

  // Sports
  {
    item_id: "5001",
    item_name: "Yoga Mat Premium",
    category: "sports",
    price: 49.99,
    brand: "ZenFit",
    description: "Extra thick yoga mat with superior grip and cushioning. Perfect for all types of yoga and exercise.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Premium%20yoga%20mat%20rolled%20up%20purple%20color%20high-quality%20texture%20sports%20equipment%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "5002",
    item_name: "Resistance Bands Set",
    category: "sports",
    price: 29.99,
    brand: "FlexPower",
    description: "Set of 5 resistance bands with different strengths. Perfect for strength training and rehabilitation.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Resistance%20bands%20set%20colorful%20bands%20different%20strengths%20sports%20equipment%20product%20photography%20clean%20background&image_size=square_hd"
  },
  {
    item_id: "5003",
    item_name: "Water Bottle 1L",
    category: "sports",
    price: 24.99,
    brand: "HydroFlow",
    description: "Insulated stainless steel water bottle keeps drinks cold for 24 hours. Leak-proof design.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Stainless%20steel%20water%20bottle%201L%20silver%20color%20insulated%20design%20sports%20equipment%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "5004",
    item_name: "Jump Rope",
    category: "sports",
    price: 19.99,
    brand: "SpeedRope",
    description: "Adjustable speed jump rope with comfortable grips. Perfect for cardio workouts and boxing training.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Adjustable%20jump%20rope%20black%20color%20comfortable%20grips%20sports%20equipment%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "5005",
    item_name: "Exercise Ball",
    category: "sports",
    price: 34.99,
    brand: "CoreBalance",
    description: "Anti-burst exercise ball for core training and stability exercises. Includes pump and exercise guide.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Exercise%20ball%20blue%20color%20anti-burst%20design%20sports%20equipment%20product%20photography&image_size=square_hd"
  },

  // Home
  {
    item_id: "6001",
    item_name: "LED Desk Lamp",
    category: "home",
    price: 39.99,
    brand: "BrightLight",
    description: "Adjustable LED desk lamp with multiple brightness levels and color temperatures. Perfect for reading and work.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Modern%20LED%20desk%20lamp%20adjustable%20arm%20white%20color%20sleek%20design%20home%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "6002",
    item_name: "Ceramic Planter Set",
    category: "home",
    price: 44.99,
    brand: "GreenThumb",
    description: "Set of 3 ceramic planters in different sizes. Perfect for indoor plants and modern home decor.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Set%20of%20ceramic%20planters%20white%20color%20different%20sizes%20modern%20design%20home%20decor%20product%20photography&image_size=square_hd"
  },
 {
    item_id: "6003",
    item_name: "Essential Oil Diffuser",
    category: "home",
    price: 32.99,
    brand: "AromaBliss",
    description: "Ultrasonic essential oil diffuser with LED mood lighting. Creates relaxing atmosphere in any room.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Essential%20oil%20diffuser%20modern%20design%20wood%20grain%20finish%20LED%20lighting%20home%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "6004",
    item_name: "Kitchen Storage Containers",
    category: "home",
    price: 56.99,
    brand: "OrganizeIt",
    description: "Set of 6 airtight storage containers with labels. Perfect for organizing pantry and keeping food fresh.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Set%20of%20kitchen%20storage%20containers%20clear%20plastic%20with%20labels%20organized%20pantry%20home%20product%20photography&image_size=square_hd"
  },
  {
    item_id: "6005",
    item_name: "Throw Pillow Set",
    category: "home",
    price: 38.99,
    brand: "CozyHome",
    description: "Set of 2 decorative throw pillows with removable covers. Soft fabric and modern geometric patterns.",
    image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Decorative%20throw%20pillows%20geometric%20patterns%20neutral%20colors%20modern%20design%20home%20decor%20product%20photography&image_size=square_hd"
  }
];

// Helper functions
function getProductsByCategory(category) {
  return products.filter(product => product.category === category);
}

function getProductById(itemId) {
  return products.find(product => product.item_id === itemId);
}

function getAllCategories() {
  return [...new Set(products.map(product => product.category))];
}

function getRandomProducts(count = 4) {
  const shuffled = [...products].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
}