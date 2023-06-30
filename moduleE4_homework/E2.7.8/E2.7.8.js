/*
Создайте произвольный массив Map.
Получите его ключи и выведите в консоль все значения в виде «Ключ — Х, значение — Y».
Используйте шаблонные строки.
*/


let map = new Map();

map.set(1, null);
map.set('str', -0);
map.set(NaN, 'qwerty');
map.set(false, true);
map.set(undefined, 78);

const keys = map.keys()

for (let key of keys) {
  console.log(`Key = ${key}, value = ${map.get(key)}`)
};
