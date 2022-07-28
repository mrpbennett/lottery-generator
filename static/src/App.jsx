import {createClient} from '@supabase/supabase-js'
import {useEffect, useState} from 'react'

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_KEY,
)

function App() {
  const [lotto, setLotto] = useState([])
  const [numbers, setNumbers] = useState([])
  const [stars, setStars] = useState([])

  //dates
  const [lottoDate, setLottoDate] = useState([])
  const [eurosDate, setEurosDate] = useState([])

  // row count
  const [lottoRowCount, setLottoRowCount] = useState([])
  const [eurosRowCount, setEurosRowCount] = useState([])

  // number generate
  const [lottoNumber, setLottoNumber] = useState([])

  const getLottoNumbers = async () => {
    await fetch('//127.0.0.1:8000/lotto')
      .then(res => res.json())
      .then(data => setLotto(data.lotto))
      .catch(err => console.log(err))
  }
  const getEuroNumbers = async () => {
    await fetch('//127.0.0.1:8000/euros')
      .then(res => res.json())
      .then(data => {
        setNumbers(data.numbers)
        setStars(data.stars)
      })
      .catch(err => console.log(err))
  }

  const getLottoDate = async () => {
    const {data, error} = await supabase
      .from('lotto_draw_history')
      .select('draw_date')

    if (error) {
      console.log(error)
    }

    setLottoDate(data)
  }
  const getEurosDate = async () => {
    const {data, error} = await supabase
      .from('euro_draw_history')
      .select('draw_date')

    if (error) {
      console.log(error)
    }

    setEurosDate(data)
  }

  const getLottoRowCount = async () => {
    const {data, error, count} = await supabase
      .from('lotto_draw_history')
      .select('*', {count: 'exact'})

    if (error) {
      console.log(error)
    }

    setLottoRowCount(count)
  }
  const getEurosRowCount = async () => {
    const {data, error, count} = await supabase
      .from('euro_draw_history')
      .select('*', {count: 'exact'})

    if (error) {
      console.log(error)
    }

    setEurosRowCount(count)
  }

  const generateLottoNumber = async () => {
    await fetch('//127.0.0.1:8000/generate-lotto')
      .then(res => res.json())
      .then(data => setLottoNumber(data))
      .catch(error => console.error(error))
  }

  useEffect(() => {
    getLottoNumbers()
    getEuroNumbers()

    // get dates of latest lotto and euros
    getLottoDate()
    getEurosDate()

    // get row count of lotto and euros
    getLottoRowCount()
    getEurosRowCount()
  }, [])

  return (
    <div className="container mx-auto mb-20 flex space-x-14">
      <div className="mt-10 flex space-x-20">
        <div>
          <h2>Lotto</h2>
          <table className="table-auto border border-blue-300 px-4">
            <thead className="bg-blue-500 text-white">
              <tr>
                <th className="px-2">Number</th>
                <th className="px-2">Count</th>
              </tr>
            </thead>
            <tbody>
              {lotto.map(number => (
                <tr key={number[0]} className="even:bg-blue-100">
                  <td className="text-center">{number[0]}</td>
                  <td className="text-center">{number[1]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="flex space-x-4">
          <div>
            <h2>Euros</h2>
            <table className="table-auto border border-blue-300 px-4">
              <thead className="bg-blue-500 text-white">
                <tr>
                  <th className="px-2">Number</th>
                  <th className="px-2">Count</th>
                </tr>
              </thead>
              <tbody>
                {numbers.map(number => (
                  <tr key={number[0]} className="even:bg-blue-100">
                    <td className="text-center">{number[0]}</td>
                    <td className="text-center">{number[1]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div>
            <h2>LuckyStars</h2>
            <table className="table-auto border border-blue-300 px-4">
              <thead className="bg-blue-500 text-white">
                <tr>
                  <th className="px-2">Star</th>
                  <th className="px-2">Count</th>
                </tr>
              </thead>
              <tbody>
                {stars.map(number => (
                  <tr key={number[0]} className="even:bg-blue-100">
                    <td className="text-center">{number[0]}</td>
                    <td className="text-center">{number[1]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="mt-10 flex flex-col space-y-5">
        <div className="text-gray-400">
          Latest Lotto draw date:{' '}
          <span className="font-mono text-gray-700">
            {lottoDate.length !== 0
              ? lottoDate[lottoDate.length - 1].draw_date
              : null}
          </span>{' '}
          with <span className="font-mono text-gray-700">{lottoRowCount}</span>{' '}
          rows of data.
        </div>

        <div className="text-gray-400">
          Latest Euros draw date:{' '}
          <span className="font-mono text-gray-700">
            {eurosDate.length !== 0 ? eurosDate[0].draw_date : null}
          </span>{' '}
          with <span className="font-mono text-gray-700">{eurosRowCount}</span>{' '}
          rows of data.
        </div>

        <div>
          <button
            className="rounded-md bg-blue-500 px-6 py-2 font-semibold text-white shadow-md"
            onClick={generateLottoNumber}
          >
            Generate lotto ticket
          </button>

          <div className="mt-10 space-x-4">
            <span className="rounded-full bg-blue-100 p-4 text-blue-800 shadow-md">
              {lottoNumber.length !== 0 ? lottoNumber[0] : '00'}
            </span>
            <span className="rounded-full bg-blue-100 p-4 text-blue-800 shadow-md">
              {lottoNumber.length !== 0 ? lottoNumber[1] : '00'}
            </span>
            <span className="rounded-full bg-blue-100 p-4 text-blue-800 shadow-md">
              {lottoNumber.length !== 0 ? lottoNumber[2] : '00'}
            </span>
            <span className="rounded-full bg-blue-100 p-4 text-blue-800 shadow-md">
              {lottoNumber.length !== 0 ? lottoNumber[3] : '00'}
            </span>
            <span className="rounded-full bg-blue-100 p-4 text-blue-800 shadow-md">
              {lottoNumber.length !== 0 ? lottoNumber[4] : '00'}
            </span>
            <span className="rounded-full bg-blue-100 p-4 text-blue-800 shadow-md">
              {lottoNumber.length !== 0 ? lottoNumber[5] : '00'}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
