import streamlit as st

st.header('Trà Sữa CoTAI')

col1,col2 = st.columns(2)
with col1:
  st.image('https://imgur.com/lEpdPsT.png')

with col2:
  size = st.radio("Kích cỡ", ('Nhỏ (30K)', 'Vừa (40K)', 'Lớn (50K)'), horizontal=True)

  st.text("Thêm")
  col3, col4, = st.columns(2)
  with col3:
    milk = st.checkbox('Sữa (5K)')
    cafe = st.checkbox('Cà phê (8K)')
  with col4:
    cream = st.checkbox('Kem (10K)')
    egg = st.checkbox('Trứng (15K)')

topping_list = 'Trân châu trắng (5K)', 'Trân châu đen (5K)', 'Thạch rau câu (6K)', 'Vải (7K)', 'Nhãn (8K)', 'Đào (10K)'
topping_price = 5,5,6,7,8,10

col5,col6 = st.columns(2)
with col5:
  toppings = st.multiselect('Topping', topping_list)
with col6:
  quantity = st.number_input('Số lượng', min_value=1, max_value=50)

note = st.text_area('Ghi chú')

if st.button('Đặt hàng', use_container_width=True):
  topping_money = sum(topping_price[i] for i in range(len(topping_list)) if topping_list[i] in toppings)
  if size == 'Nhỏ (30K)':
    price = 30
    size = 'nhỏ'
  elif size == 'Vừa (40K)':
    price = 40
    size = 'vừa'
  else:
    price = 50
    size = 'lớn'
  more = 0  # money
  more_text = []
  if milk:
    more += 5
    more_text.append('Sữa')
  if cafe:
    more += 8
    more_text.append('Cà phê')
  if cream:
    more += 10
    more_text.append('Kem')
  if egg:
    more += 15
    more_text.append('Trứng')

  more_text = ', '.join(more_text) if more > 0 else ''
  toppings = ', '.join(toppings) if topping_money > 0 else ''

  money = (price + more + topping_money) * quantity

  st.success(f'''Cỡ {size}
  \nThêm: {more_text}
  \nTopping: {toppings}
  \n{note}
  \nSố lượng: {quantity}
  \nThành tiền: {money}K''')