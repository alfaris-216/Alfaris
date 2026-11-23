/* =====================================================
   ✏️ ده الملف الوحيد اللي بتعدّل فيه الكتالوج
   - كل منتج بين { } وبينهم فاصلة
   - خانة cat لازم تطابق id القسم بالظبط:
     tyby = طبي / sosat = سوست / soft = سوفت
     sosattyby = سوست نص طبي / kavar = كفرات / me5da = مخدات
   - السعر اتركه "" لو مش عايز تظهره
   - sizes فاضية [] يعني مفيش اختيارات جاهزة،
     والعميل يكتب الطول والعرض بنفسه
   ===================================================== */
const CATALOG = {
  whatsapp: "201023010934",

  // الأقسام (id بيتكرر في كل منتج في خانة cat)
  categories: [
    { id: "tyby",      name: "طبي" },
    { id: "sosat",     name: "سوست" },
    { id: "soft",      name: "مراتب سوفت" },
    { id: "sosattyby", name: "سوست نص طبي" },
    { id: "kavar",     name: "كفرات" },
    { id: "me5da",     name: "مخدات" }
  ],

  products: [
    {
      name: "طبي",
      cat: "tyby",
      sizes: [],
      thickness: "",
      desc: "",
      price: "",
      image: ""
    },
    {
      name: "سوست",
      cat: "sosat",
      sizes: [],
      thickness: "",
      desc: "",
      price: "",
      image: ""
    },
    {
      name: "مرتبة سوفت",
      cat: "soft",
      sizes: [],
      thickness: "",
      desc: "",
      price: "",
      image: ""
    },
    {
      name: "سوست نص طبي",
      cat: "sosattyby",
      sizes: [],
      thickness: "",
      desc: "",
      price: "",
      image: ""
    },
    {
      name: "كفرات",
      cat: "kavar",
      sizes: [],
      thickness: "",
      desc: "",
      price: "",
      image: ""
    },
    {
      name: "مخدات",
      cat: "me5da",
      sizes: [],
      thickness: "",
      desc: "",
      price: "",
      image: ""
    }
  ]
};
