/**
 * 拓展JavaScript脚本
 * 从画面上读取整个表数据
 * @argument  selector  画面选择器
 * @returns   表数据
 */

var selector = arguments[0];    // 读取参数（选择器）
var result = [];
// 根据选择器获取所有行
rows = document.querySelectorAll(selector);
for (const row of rows) {
  let tdValues = [];
  for (const cell of row.children) {
    tdValues.push(cell.innerText);
  }
  result.push(tdValues);
}
return result;
