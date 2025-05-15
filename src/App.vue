<template>
  <div class="products-container">
    <!-- Фиксированная шапка -->
    <header class="header">
      <div class="counters">
        <div class="counter-item">Всего: {{ products.length }}</div>
        <div class="counter-item">Выбрано: {{ selectedProducts.length }}</div>
        <div class="counter-item">Осталось: {{ products.length - selectedProducts.length }}</div>
        <div class="counter-item">Total dump: {{ formatFileSize(totalSelectedSize) }}</div>
      </div>
      <button class="export-button" @click="exportSelected">
        Выгрузить товары с картинкой
      </button>
    </header>

    <!-- Список продуктов -->
    <div class="products-list">
      <div v-for="(product, index) in products" :key="product.article" class="product-row"
        :class="{ selected: isProductSelected(product.article) }" @click="toggleProductSelection(product)">
        <div class="product-info">
          <span class="product-number">{{ index + 1 }}.</span>
          <div class="product-details">
            <span class="product-article">Артикул: {{ product.article }}</span>
            <h3 class="product-name">{{ product.name }}</h3>
          </div>
        </div>




        <div ref="img" class="images-container" @click.stop>
          <div v-if="imgIndex % 2 !== 1" v-for="(image, imgIndex) in product.images" :key="imgIndex" class="image-wrapper" :class="{ selected: isSelectedImage(product.article, image) }"
            @click="selectImage(product.article, image, index)">
            <div class="skeleton" v-show="!loadedImages[image]">
              <div class="skeleton-animation">SMK</div>
            </div>
            <div  class="image-container" v-show="loadedImages[image]">
              <img :src="image" :alt="product.name" @load="imageLoaded(image, $event)" >
              <div class="image-info">
                {{ imageInfo[image]?.width || 0 }}x{{ imageInfo[image]?.height || 0 }},
                {{ imageInfo[image]?.size || 0 }} Кб
              </div>
            </div>
          </div>
          
        </div>


      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductsGallery',
  data() {
    return {
      // products: [],
      products: [
      {
    "article": "40085",
    "name": "Гребінці морські Вічі очищені с/м кг",
    "images": [
    "https://img.auchan.ua/rx/q_90,ofmt_webp/auchan.ua/media/catalog/product/4/0/408275286165b3bc909e00aed076f5b8fe967bc15715527541379276f844c729.jpeg"
    ]
  },
  {
    "article": "31982",
    "name": "Кальмар с/м тушка кг",
    "images": [
     "https://vitok.ua/home/catalog_products/item_2181/image/ec713457-7dee-11e9-af5f-000c2974779c.jpg"
    ]
  },
  {
    "article": "31656",
    "name": "Кальмар туба с/м кг",
    "images": [
    "https://ribnoe-remeslo.com.ua/wp-content/uploads/2019/07/krevetka-80-100.jpg"
    ]
  },
  {
    "article": "32599",
    "name": "Креветка вар/мор 90-120 кг",
    "images": [
      "https://images.prom.ua/1550481367_zamorozheni-hvosti-tigrovoyi.jpg"
    ]
  },
  {
    "article": "32644",
    "name": "Креветка вар/мор чищена з хвостом 31-40 кг",
    "images": [
      "https://vip.shuvar.com/pub/media/catalog/product/m/y/myaso-midij-vareno-morozhenoe.png"
    ]
  },
  {
    "article": "38478",
    "name": "Креветка королівська у панцирі с/м 70/80 кг",
    "images": [
      "https://vip.shuvar.com/pub/media/catalog/product/a/6/a692f7a5-9a5e-4a56-a451-1315646f8394.jpeg"
    ]
  },
  {
    "article": "32648",
    "name": "Морський коктейль с/м кг",
    "images": [
      "https://st1.stpulscen.ru/images/product/579/085/334_original.jpg"
    ]
  },
  {
    "article": "32645",
    "name": "М'ясо мідії вар/мор 100-200 кг",
    "images": [
      "https://sushist.in.ua/files/resized/products/b_grebeshok.1800x1800w.jpg"
    ]
  }
],

      loadedImages: {},
      imageInfo: {},
      selectedImagesMap: {}, // Карта выбранных изображений по артикулу
      lastSelectedImageIndex: {}, // Хранит индекс последнего выбранного изображения для каждого товара
    };
  },
  computed: {
    selectedProducts() {
      return Object.keys(this.selectedImagesMap).map(article => {
        const product = this.products.find(p => p.article === article);
        return {
          article: product.article,
          name: product.name,
          selectedImage: this.selectedImagesMap[article],
        };
      });
    },
    totalSelectedSize() {
      // Вычисляем суммарный размер всех выбранных изображений
      let totalSize = 0;

      Object.values(this.selectedImagesMap).forEach(imageUrl => {
        if (this.imageInfo[imageUrl] && this.imageInfo[imageUrl].size) {
          totalSize += this.imageInfo[imageUrl].size;
        }
      });

      return totalSize;
    }
  },
  created() {
    // this.fetchData(); //==============================================================
    this.preloadVisibleImages()
  },
  methods: {

    test() {
      scrollTo(0, 0);
    },


    async fetchData() {
      // В реальности здесь был бы запрос к API
      await fetch('/results2.json') //================================================================
        .then(response => response.json())
        .then(data => {
          console.log(data);
          
          // this.products = this.removeDuplicateLinks(data);
          this.products = data; //================================================================
        })
        .catch(error => {
          console.error('Ошибка при загрузке данных:', error);
        });
    },


    preloadVisibleImages() {
      // Загружаем только видимые изображения сначала
      this.$nextTick(() => {
        // Задержка для первых изображений каждого товара
        this.products.forEach((product, index) => {
          if (product.images && product.images.length > 0) {
            // Загружаем только первое изображение каждого товара
            setTimeout(() => {
              const img = new Image();
              const firstImage = product.images[0];
              img.onload = () => this.imageLoaded(firstImage, { target: img });
              img.src = firstImage;
            }, index * 10); // Небольшая задержка между товарами
          }
        });
      });
    },



    




    imageLoaded(imageUrl, event) {
      const img = event.target;

      // Вычисление размера изображения в килобайтах (приблизительно)
      const imgSize = this.calculateImageSize(img.naturalWidth, img.naturalHeight);

      this.$set(this.imageInfo, imageUrl, {
        width: img.naturalWidth,
        height: img.naturalHeight,
        size: Math.round(imgSize / 1024) // Округление до килобайт
      });

      this.$set(this.loadedImages, imageUrl, true);
    },

    calculateImageSize(width, height) {
      // Примерный расчет размера изображения (в байтах)
      // 4 байта на пиксель (RGBA)
      return width * height * 4;
    },

    selectImage(article, imageUrl,idx) {
      // Выбор изображения для продукта
      this.$set(this.selectedImagesMap, article, imageUrl);

      console.log( this.$refs.img[idx].scrollTo({ left: 0, behavior: 'smooth' }));
      console.log( this.$refs.img);
      

      // Сохраняем индекс выбранного изображения
      const product = this.products.find(p => p.article === article);
      if (product) {
        const imageIndex = product.images.indexOf(imageUrl);
        if (imageIndex !== -1) {
          this.$set(this.lastSelectedImageIndex, article, imageIndex);
        }
      }
    },

    isSelectedImage(article, imageUrl) {
      return this.selectedImagesMap[article] === imageUrl;
    },

    isProductSelected(article) {
      return this.selectedImagesMap.hasOwnProperty(article);
    },

    toggleProductSelection(product) {
      const article = product.article;

      if (this.isProductSelected(article)) {
        // Если товар уже выбран, удаляем его из выбранных
        this.$delete(this.selectedImagesMap, article);
        this.$delete(this.lastSelectedImageIndex, article);
      } else if (product.images && product.images.length > 0) {
        // Если товар не выбран, выбираем первое изображение
        const imageToSelect = product.images[0];
        this.selectImage(article, imageToSelect);
      }
    },

    formatFileSize(sizeInKB) {
      // Форматирование размера файла с разделителями пробелов десятых
      if (sizeInKB < 1) return '0 Кб';

      // Форматируем число с разделителем пробелов для тысяч
      return new Intl.NumberFormat('ru-RU').format(sizeInKB) + ' Кб';
    },

    exportSelected() {
      if (this.selectedProducts.length === 0) {
        alert('Нет выбранных товаров!');
        return;
      }

      const results = this.selectedProducts.map(product => ({
        article: product.article,
        name: product.name,
        selectedImage: product.selectedImage
      }));

      // Создание и скачивание файла
      const dataStr = JSON.stringify(results, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });

      const link = document.createElement('a');
      link.href = URL.createObjectURL(dataBlob);
      link.download = 'results.json';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },

    removeDuplicateLinks(jsonData) {
      // Создаем копию данных, чтобы не изменять исходный объект
      const processedData = JSON.parse(JSON.stringify(jsonData));
      
      // Обрабатываем каждый элемент в JSON
      processedData.forEach(item => {
        if (Array.isArray(item.images)) {
          // Создаем Set для отслеживания уникальных ссылок
          const uniqueLinks = new Set();
          // Создаем новый массив для хранения результата
          const filteredLinks = [];
          
          // Проходим по массиву ссылок в обратном порядке
          // чтобы сохранить последние дубликаты
          for (let i = item.images.length - 1; i >= 0; i--) {
            const link = item.images[i];
            
            // Если ссылка еще не встречалась, добавляем в результат
            if (!uniqueLinks.has(link)) {
              uniqueLinks.add(link);
              filteredLinks.unshift(link); // Добавляем в начало, чтобы сохранить порядок
            }
          }
          
          // Заменяем оригинальный массив ссылок на отфильтрованный
          item.links = filteredLinks;
        }
      });
      
      this.processedData = processedData;
      return processedData;
    }
  }
};
</script>

<style scoped>
.products-container {
  display: flex;
  flex-direction: column;
  max-width: 100%;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.header {
  position: sticky;
  top: 0;
  display: flex;
  /* justify-content: space-between; */
  align-items: center;
  padding: 15px 20px;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.counters {
  display: flex;
  gap: 20px;
  margin-right: 15px;
}

.counter-item {
  font-size: 14px;
  font-weight: bold;
}

.export-button {
  padding: 10px 15px;
  background-color: #4c5baf;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.export-button:hover {
  background-color: #4553a0;
}

.products-list {
  padding: 20px;
}

.product-row {
  height: 255px;
  display: flex;
  margin-bottom: 30px;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  cursor: pointer;
  /* transition: background-color 0.2s ease; */
}

.product-row:hover {
  background-color: #f9f9f9;
  /* overflow-x: auto; */
}

.product-row:hover .images-container {
  overflow-x: auto;
}

.product-row.selected {
  background-color: #f0f7ff;
  border: 2px solid #3498db;
}

.product-info {
  position: sticky;
  left: 0;
  width: 300px;
  padding-right: 20px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  background-color: inherit;
  z-index: 2;
}

.product-number {
  font-size: 18px;
  font-weight: bold;
  margin-right: 10px;
}

.product-details {
  display: flex;
  flex-direction: column;
}

.product-article {
  font-size: 14px;
  color: #666;
}

.product-name {
  margin: 5px 0;
  font-size: 16px;
}

.images-container {
  display: flex;
  flex-wrap: nowrap;
  gap: 15px;
  flex: 1;
  overflow-x: hidden;
  padding-bottom: 10px;
  transition: all 0.3s ease;
}

/* Стилизованный скроллбар */
.images-container::-webkit-scrollbar {
  height: 8px;
}

.images-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.images-container::-webkit-scrollbar-thumb {
  background: #3498db;
  border-radius: 10px;
}

.images-container::-webkit-scrollbar-thumb:hover {
  background: #2980b9;
}

.image-wrapper {
  position: relative;
  flex: 0 0 200px;
  height: 200px;
  border: 2px solid transparent;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
  box-sizing: content-box;
  /* transition: transform 0.2s ease; */
  /* transform: translate() scale(1); ; */
  /* Гарантирует, что padding и border не изменят размер */
}

.image-wrapper.selected {
  border-color: #5b59b1;
  order: -1;
  /* Перемещает выбранное изображение в начало */
}

.image-wrapper:hover {
  /* transform: translateY(-5px); */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.skeleton {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  display: flex;
  align-items: center;
  justify-content: center;
}

.skeleton-animation {
  font-size: 24px;
  font-weight: bold;
  color: #ccc;
}

.image-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.image-info {
  position: absolute;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  font-size: 12px;
  border-radius: 0 0 4px 0;
  z-index: 3;
  /* Убедимся, что инфо всегда поверх */
}

.image-container:hover .image-info {
  top: 0;
  /* Фиксируем позицию при наведении */
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }

  100% {
    background-position: 200% 0;
  }
}
</style>