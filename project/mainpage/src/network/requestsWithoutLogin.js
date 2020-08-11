import {requestWithoutLogin} from './baseline_configuration'

// specific request to back-end without login
export function getSingleBookmultdata1 (query) {
	return requestWithoutLogin({
		url: '/api/bookdetail/',
		params: query
	})

}

export function getCollectionmultdata1 () {
	return requestWithoutLogin({
		url: '/api/collection/'
	})

}

export function addCollection1 (query) {
	return requestWithoutLogin({
		url: '/api/collection/',
		method: 'post',
		data: query
	})

}

export function getperinfodata1 () {
	return requestWithoutLogin({
		url: '/api/account/'
	})

}

export function getCurGoal1 (query) {
	return requestWithoutLogin({
		url: '/api/set_goal/',
		params: query
	})
}

export function getSearchResult1 (query) {
	return requestWithoutLogin({
		url: '/api/searchbook/',
		method: 'post',
		data: query
	})

}

export function getSearchUserResult1 (query) {
	return requestWithoutLogin({
		url: '/api/searchbook/',
		params: query
	})

}

export function postCurGoal1 (data) {
	return requestWithoutLogin({
		url: '/api/set_goal/',
		method: 'post',
		data: data
	})
}

export function postperinfo1 (data) {
	return requestWithoutLogin({
		url: '/api/account/',
		method: 'post',
		data: data
	})

}

export function postrating1 (query) {
	return requestWithoutLogin({
		url: '/api/rating/',
		method: 'post',
		data: query
	})

}


export function Add2Collection1 (query) {
	return requestWithoutLogin({
		url: '/api/add_to_collection/',
		method: 'post',
		data: query
	})

}

export function GetReview1 (query) {
	return requestWithoutLogin({
		url: '/api/add_to_collection/',
		method: 'post',
		data: query
	})

}

export function postReview1 (query) {
	return requestWithoutLogin({
		url: '/api/review/',
		method: 'post',
		data: query
	})
}


export function postnewcollection1 (data) {
	return requestWithoutLogin({
		url: '/api/collection/',
		method: 'post',
		data: data
	})
}

export function changecollectioname1 (data) {
	return requestWithoutLogin({
		url: '/api/collection/',
		method: 'put',
		data: data
	})
}

export function delecollection1 (data) {
	return requestWithoutLogin({
		url: '/api/collection/',
		method: 'delete',
		data: data
	})
}

export function filtersearchbook1 (data) {
	return requestWithoutLogin({
		url: '/api/filter/',
		params: data
	})
}

export function delBookfromCollection1 (data) {
	return requestWithoutLogin({
		url: '/api/add_to_collection/',
		method: 'delete',
		data: data
	})
}