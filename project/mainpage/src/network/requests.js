import {request} from './baseline_configuration'
// specific request to back-end after login
export function getSingleBookmultdata (query) {
	return request({
		url: '/api/bookdetail/',
		params: query
	})

}

export function getCollectionmultdata () {
	return request({
		url: '/api/collection/'
	})

}

export function addCollection (query) {
	return request({
		url: '/api/collection/',
		method: 'post',
		data: query
	})
}

export function getAccount() {
	return request( {
		url: '/api/account/',
	})
}

export function getRecommend(query) {
	return request( {
		url: '/api/recommend/',
		params: query
	})
}

export function getperinfodata () {
	return request({
		url: '/api/account/'
	})

}

export function getCurGoal (query) {
	return request({
		url: '/api/set_goal/',
		params: query
	})
}

export function getSearchResult (query) {
	return request({
		url: '/api/searchbook/',
		method: 'post',
		data: query
	})

}

export function getSearchUserResult (query) {
	return request({
		url: '/api/searchbook/',
		params: query
	})

}

export function postCurGoal (data) {
	return request({
		url: '/api/set_goal/',
		method: 'post',
		data: data
	})
}

export function postperinfo (data) {
	return request({
		url: '/api/account/',
		method: 'post',
		data: data
	})

}

export function postrating (query) {
	return request({
		url: '/api/rating/',
		method: 'post',
		data: query
	})

}


export function Add2Collection (query) {
	return request({
		url: '/api/add_to_collection/',
		method: 'post',
		data: query
	})

}

export function GetReview (query) {
	return request({
		url: '/api/add_to_collection/',
		method: 'post',
		data: query
	})

}

export function postReview (query) {
	return request({
		url: '/api/review/',
		method: 'post',
		data: query
	})
}


export function postnewcollection (data) {
	return request({
		url: '/api/collection/',
		method: 'post',
		data: data
	})
}

export function changecollectioname (data) {
	return request({
		url: '/api/collection/',
		method: 'put',
		data: data
	})
}

export function delecollection (data) {
	return request({
		url: '/api/collection/',
		method: 'delete',
		data: data
	})
}

export function filtersearchbook (data) {
	return request({
		url: '/api/filter/',
		params: data
	})
}

export function delBookfromCollection (data) {
	return request({
		url: '/api/add_to_collection/',
		method: 'delete',
		data: data
	})
}

export function postLikeIt (query) {
	return request({
		url: '/api/likeit/',
		method: 'post',
		data: query
	})

}