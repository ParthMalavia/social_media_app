import React, { useEffect, useState } from 'react';
import {
    Box, Grid, Toolbar, List, ListItem, ListItemIcon, ListItemText, Divider,
    Avatar, Typography, Paper, TextField, Container
} from '@mui/material';
import ChatWindow from './ChatWindow';
import UseAxios from "../utils/UseAxios"
import { AUTHTOKENS, BASE_URL } from '../utils/enums';
import { jwtDecode } from 'jwt-decode';
import { useNavigate, useParams } from 'react-router-dom';


const InboxPage = () => {
    const { userId } = useParams();

    const [selectedUser, setSelectedUser] = useState(null);
    const [chatMessages, setChatMessages] = useState([]);
    const [newMessage, setNewMessage] = useState("");
    const [searchQuery, setSearchQuery] = useState('');
    const navigate = useNavigate()



    const axios = UseAxios();
    const [users, setUsers] = useState([]);

    const token = localStorage.getItem(AUTHTOKENS)
    const user_id = jwtDecode(token).user_id

    useEffect(() => {
        axios.get(`${BASE_URL}/my-inbox/${user_id}/`)
            .then(res => {
                console.log(res)
                setUsers(res.data)
            })
            .catch(err => console.log("Get Inbox Error:", err))
        
    }, [])

    function getMessages() {
        if (selectedUser) {
            axios.get(`${BASE_URL}/get-messages/${user_id}/${selectedUser.id}`)
                .then(res => setChatMessages(res.data))
                .catch(err => console.log("Get Inbox Error:", err))
        }
    }
    useEffect(() => {
        if (!userId) setSelectedUser(null)
    }, [userId])

    const handleUserClick = (user) => {
        setSelectedUser(user)
        navigate(`/inbox/${user.id}`)
    };

    useEffect(() => {
        const interval = setInterval(getMessages, 1000)
        return () => {clearInterval(interval)}
    }, [selectedUser, setSelectedUser])

    const handleSearchChange = (event) => {
        setSearchQuery(event.target.value);
    };

    function getUserProfile(user, message) {
        return (
            <ListItem
                key={user.id}
                // button
                onClick={() => handleUserClick(user)}
            >
                <ListItemIcon>
                    <Avatar src={user.image} />
                </ListItemIcon>
                <ListItemText>
                    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                        <Typography variant="body1">{user.full_name}</Typography>
                        <Typography variant="caption">{message}</Typography>
                    </Box>
                </ListItemText>
            </ListItem>
        )
    }

    function sendMessage() {
        console.log("Send message called")
        const formData = new FormData()
        formData.append("user", user_id)
        formData.append("sender", user_id)
        formData.append("receiver", userId)
        formData.append("message", newMessage)
        axios.post(`${BASE_URL}/send-message/`, formData)
            .then(res => {
                console.log(res)
                setNewMessage("")
            })
            .catch(err => console.log("Send Message Error::", err))
        
        
    }

    return (
        <Container>
            <Paper sx={{margin: 2}}>
                <Typography variant="h6" component="div" padding={2} >
                    Messenger
                </Typography>
                <Box sx={{ display: 'flex' }}>
                    <Grid container spacing={2}>
                        <Grid item xs={4}>
                            <Toolbar>
                                <TextField
                                    label="Search"
                                    variant="outlined"
                                    value={searchQuery}
                                    onChange={handleSearchChange}
                                    fullWidth
                                />
                            </Toolbar>
                            <List>
                                {users.map(user => {
                                    if (user.sender === user_id) {
                                        return getUserProfile(user.receiver_profile, user.message)
                                    }
                                    return getUserProfile(user.sender_profile, user.message)
                                }
                                )}

                            </List>
                        </Grid>
                        <Grid item xs={8}>
                            {selectedUser && (
                                <ChatWindow
                                    recipient={selectedUser}
                                    messages={chatMessages}
                                    user_id={user_id}
                                    newMessage={newMessage}
                                    setNewMessage={setNewMessage}
                                    sendMessage={sendMessage}
                                />
                            )}
                        </Grid>
                    </Grid>
                </Box>
            </Paper>
        </Container>
    );
};

export default InboxPage;
