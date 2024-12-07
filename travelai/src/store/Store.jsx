import {configurateStore} from 'redux';

const initialState = {
    listTours: [],
    user: {name: '', surname: ''},
    favorite: [],
    isAuthed: true,

};

const store = configurateStore({
    state: initialState,
    reducers: [],
    middlewares: [],
})