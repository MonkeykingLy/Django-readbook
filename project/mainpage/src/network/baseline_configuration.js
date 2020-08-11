import axios from 'axios'
// baseline_configuration for login request to back-end
export function request (config) {
	//create instance of axios
	const instance = axios.create({
		baseURL: 'http://127.0.0.1:8000',
		timeout: 5000

	})

	//axios  interceptor request
	instance.interceptors.request.use(config => {
		// console.log(config)
		config.headers.Authorization = 'Token ' + window.localStorage.getItem('token')

		return config
	}, err => {
		console.log(err)

	})
	//axios  interceptor response
	instance.interceptors.response.use(res => {
		return res.data
	}, err => {
		return Promise.resolve(err.response)
		// console.log(err)

	})
	// real request
	return instance(config)

}

// baseline_configuration for without login request to back-end
export function requestWithoutLogin (config) {
	//create instance of axios
	const instance = axios.create({
		baseURL: 'http://127.0.0.1:8000',
		timeout: 5000

	})

	//axios  interceptor request
	instance.interceptors.request.use(config => {
		// console.log(config)
		return config
	}, err => {
		console.log(err)

	})
	//axios  interceptor response
	instance.interceptors.response.use(res => {
		return res.data
	}, err => {
		return Promise.resolve(err.response)
		// console.log(err)

	})
	// real request
	return instance(config)

}




