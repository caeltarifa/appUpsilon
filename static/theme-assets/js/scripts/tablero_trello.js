function _extends() {_extends = Object.assign || function (target) {for (var i = 1; i < arguments.length; i++) {var source = arguments[i];for (var key in source) {if (Object.prototype.hasOwnProperty.call(source, key)) {target[key] = source[key];}}}return target;};return _extends.apply(this, arguments);}const { useEffect, useState } = React;
const { DragDropContext, Draggable, Droppable } = ReactBeautifulDnd;

const DATA = [
{
  id: 'af1',
  label: 'BOV543-IS',
  items: [
  { id: 'af2', label: 'Item 1' },
  { id: 'af3', label: 'Item 2' },
  { id: 'af44', label: 'Item 3' },
  { id: 'af55', label: 'Item 4' },
  { id: 'af66', label: 'Item 5' },
  { id: 'af77', label: 'Item 6' }],

  tint: 1 },

{
  id: 'af4',
  label: 'BOV653-IS',
  items: [
  { id: 'af5', label: 'Item 1' },
  { id: 'af6', label: 'Item 2' }],

  tint: 2 },

{
  id: 'af7', 
  label: 'ECO329-IS',
  items: [
  { id: 'af8', label: 'Item 1' },
  { id: 'af9', label: 'Item 2' }],

  tint: 3 }];
  



  const DATA2 = [
    {
      id: 'af1',
      label: 'BOV543-IS',
      items: [
      { id: 'af2', label: 'Item 1' },
      { id: 'af3', label: 'Item 2' },
      { id: 'af4', label: 'Item 1' },
      { id: 'af5', label: 'Item 2' },
      { id: 'af6', label: 'Item 1' },
      { id: 'af7', label: 'Item 2' }],
    
      tint: 1 },
    
    {
      id: 'af8', 
      label: 'ECO329-IS',
      items: [
      { id: 'af9', label: 'Item 1' },
      { id: 'af10', label: 'Item 2' }],
    
      tint: 2 }];




function App()
{
  return (
    React.createElement("div", { className: "layout__wrapper" },
    React.createElement("div", { className: "layout__header" },
    React.createElement("div", { className: "app-bar" },
    React.createElement("div", { className: "app-bar__title" }, "FIR LA PAZ"))),


    React.createElement(LeadsOverview, null)));


}

function LeadsOverview() {
  const [items, setItems] = useState([]);
  const [groups, setGroups] = useState({});

  useEffect(() => {
    // Mock an API call.
    buildAndSave(DATA2);
  }, []);
// NUCLE4R@44s4n4
  function buildAndSave(items)
  {
    const groups = {};
    for (let i = 0; i < Object.keys(items).length; ++i) {
      const currentGroup = items[i];
      groups[currentGroup.id] = i;
    }

    // Set the data.
    setItems(items);

    // Makes the groups searchable via their id.
    setGroups(groups);
  }

  return (
    React.createElement(DragDropContext, {
      onDragEnd: result => {
        const { destination, draggableId, source, type } = result;

        if (!destination) {
          return;
        }

        if (destination.droppableId === source.droppableId && destination.index === source.index) {
          return;
        }

        if ('group' === type) {
          const sourceIndex = source.index;
          const targetIndex = destination.index;

          const workValue = items.slice();
          const [deletedItem] = workValue.splice(sourceIndex, 1);
          workValue.splice(targetIndex, 0, deletedItem);

          buildAndSave(workValue);

          return;
        }

        const sourceDroppableIndex = groups[source.droppableId];
        const targetDroppableIndex = groups[destination.droppableId];
        const sourceItems = items[sourceDroppableIndex].items.slice();
        const targetItems = source.droppableId !== destination.droppableId ? items[targetDroppableIndex].items.slice() : sourceItems;

        // Pull the item from the source.
        const [deletedItem] = sourceItems.splice(source.index, 1);
        targetItems.splice(destination.index, 0, deletedItem);

        const workValue = items.slice();
        workValue[sourceDroppableIndex] = {
          ...items[sourceDroppableIndex],
          items: sourceItems };

        workValue[targetDroppableIndex] = {
          ...items[targetDroppableIndex],
          items: targetItems };



        setItems(workValue);
      } },

    React.createElement(Droppable, { droppableId: "ROOT", type: "group" },
    (provided) =>
    React.createElement("div", _extends({},
    provided.droppableProps, {
      ref: provided.innerRef }),

    items.map((item, index) =>
    React.createElement(Draggable, {
      draggableId: item.id,
      key: item.id,
      index: index },

    (provided) =>
    React.createElement("div", _extends({},
    provided.draggableProps,
    provided.dragHandleProps, {
      ref: provided.innerRef }),

    React.createElement(DroppableList, _extends({
      key: item.id },
    item))))),


    provided.placeholder))));




}

function DroppableList({ id, items, label, tint })
{
  return (
    React.createElement(Droppable, { droppableId: id },
    (provided) =>
    React.createElement("div", _extends({},
    provided.droppableProps, {
      ref: provided.innerRef }),

    React.createElement("div", { className: `holder holder--tint-${tint}` },
    React.createElement("div", { className: "holder__title" },
    label),

    React.createElement("div", { className: "holder__content" },
    React.createElement("ul", { className: "list" },
    items.map((item, index) =>
    React.createElement("li", {
      className: "list__item",
      key: item.id },

    React.createElement(Draggable, {
      draggableId: item.id,
      index: index },

    (provided) =>
    React.createElement("div", _extends({
      className: "cardficha" },
    provided.draggableProps,
    provided.dragHandleProps, {
      ref: provided.innerRef }),

    item.label)))),





    provided.placeholder))))));







}

ReactDOM.render(React.createElement(App, null), document.getElementById('root'));
ReactDOM.render(React.createElement(App, null), document.getElementById('root2'));
ReactDOM.render(React.createElement(App, null), document.getElementById('root3'));










// dragula([			
//     document.getElementById('1')			
//     ])			
                
//     .on('drag', function(el) {			
//     // add 'is-moving' class to element being dragged			
//     el.classList.add('is-moving');			
//     })			
//     .on('dragend', function(el) {			
//     // remove 'is-moving' class from element after dragging has stopped			
//     el.classList.remove('is-moving');			
//     // add the 'is-moved' class for 600ms then remove it			
//     window.setTimeout(function() {			
//     el.classList.add('is-moved');			
//     window.setTimeout(function() {			
//     el.classList.remove('is-moved');			
//     }, 600);			
//     }, 100);			
//     });			
                
                
                
//     createOptions.create();			
//     showOptions.init();			