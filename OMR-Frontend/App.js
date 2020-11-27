
import React, {useState,useEffect} from 'react';
import { StyleSheet, Text, Button,SafeAreaView,Alert,Image, View,ScrollView } from 'react-native';
// import DocumentScanner from 'react-native-documentscanner-android';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import * as ImagePicker from 'expo-image-picker';
import * as BackgroundFetch from 'expo-background-fetch';
import mime from "mime";


const arr2=[{"Student1":"one",
  "marks":10
},{"Student1":"one",
  "marks":10
},{"Student1":"two",
  "marks":10
},{"Student1":"3",
  "marks":10
}]

const CardComponent = ( {data }) => {
 
  return (
    <>

      {data.map((data, index) => {
        return (
         
             <View key={index} style={{flex:1,justifyContent:"center"}}>
             <View style={{padding:10,textAlign:"center"}}>
         
        <Text style={{textAlign:"center"}}>Student {index+1} </Text>
              <Text style={{textAlign:"center"}}>Enrollment ID:{data.Enrollment_ID}</Text>
              <Text style={{textAlign:"center"}}>Test ID:{data.Test_ID}</Text>
              <Text style={{textAlign:"center"}}>Marks Scored:{data.Grade}</Text>
              <Text style={{textAlign:"center"}}>Aggregate %:{data.aggr_score}</Text>
              </View>
              </View>
          
           
          
          
        );
     })}
     
    </>
  );

};
function DetailsScreen({ navigation }) {
  const [data1,setData1]=React.useState([])
  

      useEffect(() => {
        fetch("http://192.168.0.104:5000/omrread/").then(response => response.json()).then(response => {
          console.log("upload succes", response);
          
          setData1(response)
          console.log(data1)
          
        })
        .catch(error => {
          console.log("upload error", error);
          alert("Failed to fetch results",error);
        });
        
    }, [])
      
   
  
  // setData1(arr2)
  return (
   
      <View style={{flex:1,justifyContent:"center",backgroundColor:"#fff", alignItems:"stretch"}}>
      
      <Text style={{fontSize:30,padding:10,textAlign:"center"}}>View Your Results</Text> 
      
      <ScrollView>
      
      
    <CardComponent data={data1}></CardComponent>
    </ScrollView>
    
    
  </View>
    
     
      
      
      
   
  );
}

var Answerres ;
var OMRKEY;


function OMRPicker({ navigation }) {
  const [image, setImage] = useState(null);
  const [imageDict, setImageDict] = useState({});
  const[imageUri,setUri]=useState(null);

   const createFormData = (photo,body) => {
    console.log("Debug1");
    const data = new FormData();
    console.log("Debug2");
    data.append("photo", {
      name: ("file:///" + photo.uri.split("file:/").join()).split("/").pop(),
      type: mime.getType("file:///" + photo.uri.split("file:/").join("")),
      uri:
          "file:///" + photo.uri.split("file:/").join("") 
    });

    Object.keys(body).forEach(key => {
      data.append(key, body[key]);
    });
  
    console.log("Debug3");
    console.log(data);
  
    return data;
  };
  

  useEffect(() => {
    (async () => {
      if (Platform.OS !== 'web') {
        const { status } = await ImagePicker.requestCameraRollPermissionsAsync();
        if (status !== 'granted') {
          alert('Sorry, we need camera roll permissions to make this work!');
        }
      }
    })();
  }, []);
  
  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: true,
      
      quality: 1,
    });
    
    console.log(result);
    

    if (!result.cancelled) {
      setImageDict(result)
      setImage(result.uri);
      
      setUri(result.uri)
    }
  };
  const UploadOMR = async () => {
    fetch("http://YOUR_IP:5000/omrread/", {
      method: "POST",
      headers: {
        "Content-Type": "multipart/form-data"
    },
      body: createFormData(imageDict, { userId: "123" })
    })
      .then(response => response.json())
      .then(response => {
        console.log("upload succes", response);
        alert(response.args);
        navigation.navigate('Home')
      })
      .catch(error => {
        console.log("upload error", error);
        alert("Upload failed!,Try Again");
      });
    
   
  };

  

  return (
    
    <View style={{flex:1,justifyContent:"center",backgroundColor:"#fff", alignItems:"stretch"}}>
    
      <Button title="Pick the OMR Answer Sheets" onPress={pickImage} />
      <View style={{flex:1,justifyContent:"center"}}>
     
      <Text >
      {imageUri}
      </Text>
      
     
      </View>
      
      
      <View style={{flex:1,justifyContent:"center"}}>
      <Button title="Upload OMR's" onPress={UploadOMR}/>
      </View>
    </View>
    
  );
}


function AnswerPicker({ navigation }) {
  const [image, setImage] = useState(null);
  const [imageDict, setImageDict] = useState({});

  
  const[KeyUri,setKeyUri]=useState(null);
  const createFormData = (photo,body) => {
    console.log("Debug1");
    const data = new FormData();
    console.log("Debug2");
    data.append("photo", {
      name: ("file:///" + photo.uri.split("file:/").join()).split("/").pop(),
      type: mime.getType("file:///" + photo.uri.split("file:/").join("")),
      uri:
          "file:///" + photo.uri.split("file:/").join("") 
    });

    Object.keys(body).forEach(key => {
      data.append(key, body[key]);
    });
  
    console.log("Debug3");
    console.log(data);
  
    return data;
  };

  useEffect(() => {
    (async () => {
      if (Platform.OS !== 'web') {
        const { status } = await ImagePicker.requestCameraRollPermissionsAsync();
        if (status !== 'granted') {
          alert('Sorry, we need camera roll permissions to make this work!');
        }
      }
    })();
  }, []);

  
  

  const pickAnswer = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: true,
      
      quality: 1,
    });
    
    console.log(result);
    console.log(OMRKEY);
    console.log(imageDict);

    if (!result.cancelled) {

      setImageDict(result)
      setImage(result.uri);
      OMRKEY=image;
      setKeyUri(OMRKEY)
    }
  };
  const UploadAnswer = async () => {

    fetch("http://YOUR_IP:5000/answer_read/", {
      method: "POST",
      headers: {
        "Content-Type": "multipart/form-data"
    },
      body: createFormData(imageDict, { userId: "123" })
    })
      .then(response => response.json())
      .then(response => {
        console.log("upload succes", response);
        alert(response.args);
        navigation.navigate('Home')
      })
      .catch(error => {
        console.log("upload error", error);
        alert("Upload failed!,Try Again");
      });
    
  };
  

  return (
    
    <View style={{flex:1,justifyContent:"center",backgroundColor:"#fff", alignItems:"stretch"}}>
    
     
      <Button title="Pick the AnswerKey" onPress={pickAnswer} />
      <View style={{flex:1,justifyContent:"center"}}>
      <Text >
      {KeyUri}
      </Text>
      </View>
      
      <View style={{flex:1,justifyContent:"center"}}>
      <Button title="Upload AnswerKey" onPress={UploadAnswer}/>
      </View>
    </View>
    
  );
}





function HomeScreen({ navigation }) {
  
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
   
      <Button
      title="Choose AnswerKey"
      onPress={() => navigation.navigate('AnswerPicker')}
    />
   
      <Button
      title="Choose Response Sheets"
      onPress={() => navigation.navigate('OMRPicker')}
    />
     <Button
        title="Check Results"
        onPress={() => navigation.navigate('Results')}
      />
    </View>
  );
}
const Stack = createStackNavigator();

export default function App({ navigation }) {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Results" component={DetailsScreen} />
        <Stack.Screen name="AnswerPicker" component={AnswerPicker} />
        <Stack.Screen name="OMRPicker" component={OMRPicker} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}



const styles = StyleSheet.create({
  title:{
   fontSize:40,
    color: 'black',
    justifyContent: 'center',
    
  },
  button:{
    
    marginTop: 50,
  },

  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
