import { useState } from 'react'
import axios from 'axios'
import BootstrapTable from 'react-bootstrap-table-next'
import paginationFactory from 'react-bootstrap-table2-paginator'

import 'react-bootstrap-table2-paginator/dist/react-bootstrap-table2-paginator.min.css'

const Buylist = () => {

  const columns = [
    {
      dataField: 'cardName',
      text: 'Card',
      sort: true
    },
    {
      dataField: 'seller',
      text: 'Seller',
      formatter: (cell, row) => {
        return <a href={row.href}>{cell}</a>
      },
      sort: true
    },
    {
      dataField: 'condition',
      text: 'Condition',
      sort: true
    },
    {
      dataField: 'price',
      text: 'Price',
      formatter: (cell, row) => {
        return row.og_price ? 
          <span><strike>R$ {row.og_price}</strike><br/>R$ {cell}</span>
          : `R$ ${cell}`
      },
      sort: true
    },
    {
      dataField: 'edition',
      text: 'Edition',
      sort: true
    },
    {
      dataField: 'language',
      text: 'Language',
      sort: true
    },
    {
      dataField: 'extras',
      text: 'Extras',
      formatter: cell => cell.join(", "),
      sort: true
    }
  ]

  const [cardText, setCardText] = useState('')
  const [isLoading, setLoading] = useState(false)
  const [cardList, setCardList] = useState(undefined)

  const [sellersFilter, setSellersFilter] = useState({})

  const searchCard = async (cardName) => {
    const url = `http://localhost:5000/price?card=${cardName}`
    const { data } = await axios.get(url)
    return data
  }

  const fetchCards = async (cards) => {
    const response = await Promise.allSettled(cards.map(searchCard))
    return cards.map((cardName, idx) => ({...response[idx], cardName }))
  }

  const handleSearch = async () => {
    setCardList(undefined)
    setLoading(true)

    const cards = cardText.split('\n')
    const response = await fetchCards(cards)
    const fetchFulfilled = response.filter(item => item.status === 'fulfilled')
    const data = fetchFulfilled.map(cardResult => {
      return cardResult.value.map(item => ({cardName: cardResult.cardName, ...item}))
    }).flat()

    setLoading(false)
    setCardList(data)

    // const sellers = Array.from(new Set(data.map(item => item.seller))).reduce((acc, cur, idx) => ({...acc, [idx]: cur}), {})
    // setSellersFilter(sellers)
  }

  return (
    <div className='container flex'>

      {/* Textarea to write cards */}
      <div>
        <textarea
          name='cards-list'
          type='text'
          placeholder='Lista de cartas'
          style={{ height: '50vh', width: '100%', resize: 'none' }}
          value={cardText}
          onChange={e => setCardText(e.target.value)}
        />
      </div>

      {/* Button to search cards */}
      <div className='mt-3'>
        <button
          className='btn btn-primary'
          onClick={handleSearch}
        >
          Pesquisar
        </button>
      </div>

      {/* Progress bar */}
      {isLoading ? (
        <></>
      ) : (
        <></>
      )}

      {/* DataTable */}
      {cardList ? (
        <div className='mt-5'>
          <BootstrapTable
            keyField='id'
            data={cardList.map((item, index) => ({id: index, ...item}))}
            columns={columns}
            pagination={paginationFactory()}
          />
        </div>
      ) : (
        <></>
      )}

    </div>
  )
}

export default Buylist;