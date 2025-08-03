CREATE TABLE "users"(
    "id" BIGINT NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "is_staff" BOOLEAN NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "date_joinded" DATE NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("id");
CREATE TABLE "categories"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "slug" VARCHAR(255) NOT NULL,
    "created_at" DATE NOT NULL
);
ALTER TABLE
    "categories" ADD PRIMARY KEY("id");
CREATE TABLE "products"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "price" INTEGER NOT NULL,
    "stock" INTEGER NOT NULL,
    "image" VARCHAR(255) NOT NULL,
    "created_at" DATE NOT NULL,
    "category_id" BIGINT NOT NULL
);
ALTER TABLE
    "products" ADD PRIMARY KEY("id");
ALTER TABLE
    "products" ADD CONSTRAINT "products_category_id_unique" UNIQUE("category_id");
CREATE TABLE "orders"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "total_price" DECIMAL(8, 2) NOT NULL,
    "status" VARCHAR(255) NOT NULL,
    "created_at" DATE NOT NULL
);
ALTER TABLE
    "orders" ADD PRIMARY KEY("id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_user_id_unique" UNIQUE("user_id");
CREATE TABLE "order_items"(
    "id" BIGINT NOT NULL,
    "order_id" BIGINT NOT NULL,
    "product_id" BIGINT NOT NULL,
    "quantity" BIGINT NOT NULL,
    "price" DECIMAL(8, 2) NOT NULL
);
ALTER TABLE
    "order_items" ADD PRIMARY KEY("id");
ALTER TABLE
    "order_items" ADD CONSTRAINT "order_items_order_id_unique" UNIQUE("order_id");
ALTER TABLE
    "order_items" ADD CONSTRAINT "order_items_product_id_unique" UNIQUE("product_id");
CREATE TABLE "cart_items"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "product_id" BIGINT NOT NULL,
    "quantity" INTEGER NOT NULL
);
ALTER TABLE
    "cart_items" ADD PRIMARY KEY("id");
ALTER TABLE
    "cart_items" ADD CONSTRAINT "cart_items_user_id_unique" UNIQUE("user_id");
ALTER TABLE
    "cart_items" ADD CONSTRAINT "cart_items_product_id_unique" UNIQUE("product_id");
CREATE TABLE "shipping_addresses"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "address_line1" VARCHAR(255) NOT NULL,
    "address_line2" VARCHAR(255) NOT NULL,
    "city" VARCHAR(255) NOT NULL,
    "state" VARCHAR(255) NOT NULL,
    "postal_code" VARCHAR(255) NOT NULL,
    "country" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "shipping_addresses" ADD PRIMARY KEY("id");
ALTER TABLE
    "shipping_addresses" ADD CONSTRAINT "shipping_addresses_user_id_unique" UNIQUE("user_id");
ALTER TABLE
    "shipping_addresses" ADD CONSTRAINT "shipping_addresses_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "cart_items" ADD CONSTRAINT "cart_items_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "order_items" ADD CONSTRAINT "order_items_order_id_foreign" FOREIGN KEY("order_id") REFERENCES "orders"("id");
ALTER TABLE
    "order_items" ADD CONSTRAINT "order_items_product_id_foreign" FOREIGN KEY("product_id") REFERENCES "products"("id");
ALTER TABLE
    "products" ADD CONSTRAINT "products_category_id_foreign" FOREIGN KEY("category_id") REFERENCES "categories"("id");
ALTER TABLE
    "cart_items" ADD CONSTRAINT "cart_items_product_id_foreign" FOREIGN KEY("product_id") REFERENCES "products"("id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");