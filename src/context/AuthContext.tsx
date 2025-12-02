'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { initializeApp, getApps, getApp } from 'firebase/app';
import { getAuth, onAuthStateChanged, User as FirebaseUser } from 'firebase/auth';
import { getFirestore, doc, setDoc } from 'firebase/firestore';

// Configuração do Firebase fornecida pelo usuário
const firebaseConfig = {
  apiKey: "AIzaSyC1yhQuFMOxsyy8KROjHw-DiqCyzXVyEF0",
  authDomain: "sacy-ia.firebaseapp.com",
  projectId: "sacy-ia",
  storageBucket: "sacy-ia.firebasestorage.app",
  messagingSenderId: "550826387693",
  appId: "1:550826387693:web:98582b80769b386768c4e4"
};

// ID da Aplicação (usando o appId do firebaseConfig)
const appId = "1:550826387693:web:98582b80769b386768c4e4";

// Inicializa o Firebase
let app;
if (!getApps().length) {
  app = initializeApp(firebaseConfig);
} else {
  app = getApp();
}

const auth = getAuth(app);
const db = getFirestore(app);

// Tipagem para o Contexto
interface AuthContextType {
  user: FirebaseUser | null;
  loading: boolean;
  db: any; // Firestore instance
  auth: any; // Auth instance
  appId: string; // Application ID
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Hook personalizado para usar o contexto
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Componente Provedor de Autenticação
interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<FirebaseUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Subscreve-se às mudanças de estado de autenticação
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false); // Torna-se false assim que o Firebase verifica o estado
    });

    // Limpeza da subscrição
    return () => unsubscribe();
  }, []);

  // O provedor só renderiza os children quando !loading
  if (loading) {
    // Retorna um div simples enquanto carrega
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>A carregar...</div>;
  }

  const value = {
    user,
    loading,
    db,
    auth,
    appId,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Exporta as funções de manipulação do Firestore para o registro
export const createUserProfile = async (user: FirebaseUser) => {
  const userRef = doc(db, "artifacts", appId, "users", user.uid, "profile");
  await setDoc(userRef, {
    email: user.email,
    createdAt: new Date().toISOString(),
    // Adicione outros campos de perfil aqui, se necessário
  }, { merge: true });
};
