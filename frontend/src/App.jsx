import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState({ name: '', price: 0, quantity: 0 });
  const [editingItem, setEditingItem] = useState(null);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    const res = await axios.get('http://localhost:8000/items');
    setItems(res.data);
  };

  const addItem = async () => {
    await axios.post('http://localhost:8000/items', newItem);
    fetchItems();
    setNewItem({ name: '', price: 0, quantity: 0 });
  };

  const updateItem = async (id) => {
    await axios.put(`http://localhost:8000/items/${id}`, editingItem);
    fetchItems();
    setEditingItem(null);
  };

  const deleteItem = async (id) => {
    await axios.delete(`http://localhost:8000/items/${id}`);
    fetchItems();
  };

  const updateQuantity = async (id, action) => {
    await axios.put(`http://localhost:8000/items/${id}/quantity?action=${action}`);
    fetchItems();
  };

  return (
    <div>
      <h1>Grocery Store</h1>
      <ul>
        {items.map(item => (
          <li key={item.name}>
            {item.name} - ${item.price} - Quantity: {item.quantity}
            <button onClick={() => updateQuantity(item._id, 'add')}>+1</button>
            <button onClick={() => updateQuantity(item._id, 'remove')}>-1</button>
            <button onClick={() => setEditingItem(item)}>Edit</button>
            <button onClick={() => deleteItem(item._id)}>Delete</button>
          </li>
        ))}
      </ul>
      <h2>Add/Update Item</h2>
      <input
        placeholder="Name"
        value={editingItem ? editingItem.name : newItem.name}
        onChange={e => editingItem ? setEditingItem({...editingItem, name: e.target.value}) : setNewItem({...newItem, name: e.target.value})}
      />
      <input
        type="number"
        placeholder="Price"
        value={editingItem ? editingItem.price : newItem.price}
        onChange={e => editingItem ? setEditingItem({...editingItem, price: parseFloat(e.target.value)}) : setNewItem({...newItem, price: parseFloat(e.target.value)})}
      />
      <input
        type="number"
        placeholder="Quantity"
        value={editingItem ? editingItem.quantity : newItem.quantity}
        onChange={e => editingItem ? setEditingItem({...editingItem, quantity: parseInt(e.target.value)}) : setNewItem({...newItem, quantity: parseInt(e.target.value)})}
      />
      <button onClick={editingItem ? () => updateItem(editingItem._id) : addItem}>
        {editingItem ? 'Update' : 'Add'}
      </button>
    </div>
  );
}

export default App;